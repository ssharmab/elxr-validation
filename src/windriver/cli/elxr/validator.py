from argparse import Namespace
import contextlib
import logging
import time

import pexpect
#from lava_dispatcher.device import NewDevice
from lava_common.exceptions import ConnectionClosedError, InfrastructureError, JobError, LAVABug, TestError
from lava_common.log import YAMLLogger
from lava_common.timeout import Timeout
from lava_dispatcher.connection import Connection
from lava_dispatcher.device import  NewDevice, PipelineDevice
from lava_dispatcher.parser import JobParser
from lava_dispatcher.job import Job
from collections import namedtuple
from lava_dispatcher.shell import ShellCommand, ShellSession
from lava_dispatcher.utils.strings import seconds_to_str

logging.setLoggerClass(YAMLLogger)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)

Options = namedtuple('Options', ['definition', 'device', 'dispatcher', 'env_dut'])

class Validator:
    def validate(self, device_path):
        stream = open(device_path, 'r').read()
        options = Options(stream, {}, None, None)
        
        job : Job = parse_job_file(logger, options)
        job.validate()
        
        # shell_command = ShellCommand("/bin/bash", Timeout(6600), logger = logger)
        # connection = ShellSession(None, shell_command)
        
        
        job.run()

class ThisDevice(PipelineDevice):
    def __init__(self):
        self.setdefault("power_state", "on")
        self.setdefault("dynamic_data", {})
        self.setdefault("actions", {
            "run": True,
            "boot": {
                "serial": True,
                "methods": [
                    "minimal"
                ]
            },
            "deploy": {
                "methods": [
                    "overlay"
                ]
            }
        })
        self.setdefault("constants", {
            'default-shell-prompt': ".*[a-zA-Z0-9_]+@.*# $",
            'failure_retry': None,
            'posix': {
                "line_separator": "\n",
                "distro": "debian",
                "tar_flags": "--warning no-timestamp",
                "lava_test_sh_cmd": "/bin/bash",
                "lava_test_dir": "/lava-%s",
                "lava_test_results_part_attr": "root_part",
                "lava_test_results_dir": "/lava-%s",
                "lava_test_shell_file": "~/.bashrc",
            }
        })

def parse_job_file(logger, options: Options) -> Job:
    """
    Uses the parsed device_config instead of the old Device class
    so it can fail before the Pipeline is made.
    Avoids loading all configuration for all supported devices for every job.
    """
    # Prepare the pipeline from the file using the parser.
    device = NewDevice("device.yaml")
    parser = JobParser()

    # Load the configuration files (this should *not* fail)
    env_dut = None
    if options.env_dut is not None:
        env_dut = options.env_dut.read()
    dispatcher_config = None
    if options.dispatcher is not None:
        dispatcher_config = options.dispatcher.read()

    # Generate the pipeline
    return parser.parse(
        options.definition,
        device,
        1,
        logger=logger,
        dispatcher_config=None,
        env_dut=None,
    )


class ShellConnection(Connection):
    name = "ShellSession"

    def __init__(self):
        """
        A ShellSession monitors a pexpect connection.
        Optionally, a prompt can be forced after
        a percentage of the timeout.
        """
        shell_command = ShellCommand("/bin/bash", Timeout(6600), logger = logger)
        
        super().__init__(shell_command)
        # FIXME: rename __prompt_str__ to indicate it can be a list or str
        self.__prompt_str__ = None
        self.spawn = shell_command
        self.__runner__ = None
        self.timeout = shell_command.lava_timeout
        self.__logger__ = None
        self.tags = ["shell"]

    @property
    def logger(self):
        if not self.__logger__:
            self.__logger__ = logging.getLogger("dispatcher")
        return self.__logger__

    # FIXME: rename prompt_str to indicate it can be a list or str
    @property
    def prompt_str(self):
        return self.__prompt_str__

    @prompt_str.setter
    def prompt_str(self, string):
        """
        pexpect allows the prompt to be a single string or a list of strings
        this property simply replaces the previous value with the new one
        whether that is a string or a list of strings.
        To use + the instance of the existing prompt_str must be checked.
        """
        self.logger.debug("Setting prompt string to %r" % string)
        self.__prompt_str__ = string

    @contextlib.contextmanager
    def test_connection(self):
        """
        Yields the actual connection which can be used to interact inside this shell.
        """
        yield self.raw_connection

    def force_prompt_wait(self, remaining=None):
        """
        One of the challenges we face is that kernel log messages can appear
        half way through a shell prompt.  So, if things are taking a while,
        we send a newline along to maybe provoke a new prompt.  We wait for
        half the timeout period and then wait for one tenth of the timeout
        6 times (so we wait for 1.1 times the timeout period overall).
        :return: the index into the connection.prompt_str list
        """
        prompt_wait_count = 0
        if not remaining:
            return self.wait()
        # connection_prompt_limit
        partial_timeout = remaining / 2.0
        self.logger.debug(
            "Waiting using forced prompt support (timeout %s)"
            % seconds_to_str(partial_timeout)
        )
        while True:
            try:
                return self.raw_connection.expect(
                    self.prompt_str, timeout=partial_timeout
                )
            except (pexpect.TIMEOUT, TestError) as exc:
                if prompt_wait_count < 6:
                    self.logger.warning(
                        "%s: Sending %s in case of corruption. Connection timeout %s, retry in %s",
                        exc,
                        self.check_char,
                        seconds_to_str(remaining),
                        seconds_to_str(partial_timeout),
                    )
                    self.logger.debug("pattern: %s", self.prompt_str)
                    prompt_wait_count += 1
                    partial_timeout = remaining / 10
                    self.sendline(self.check_char)
                    continue
                else:
                    # TODO: is someone expecting pexpect.TIMEOUT?
                    raise
            except ConnectionClosedError as exc:
                self.connected = False
                raise InfrastructureError(str(exc))

    def wait(self, max_end_time=None, max_searchwindowsize=False):
        """
        Simple wait without sendling blank lines as that causes the menu
        to advance without data which can cause blank entries and can cause
        the menu to exit to an unrecognised prompt.
        """
        if not max_end_time:
            timeout = self.timeout.duration
        else:
            timeout = max_end_time - time.monotonic()
        if timeout < 0:
            raise LAVABug("Invalid max_end_time value passed to wait()")
        try:
            if max_searchwindowsize:
                return self.raw_connection.expect(
                    self.prompt_str, timeout=timeout, searchwindowsize=None
                )
            else:
                return self.raw_connection.expect(self.prompt_str, timeout=timeout)
        except (TestError, pexpect.TIMEOUT):
            raise JobError("wait for prompt timed out")
        except ConnectionClosedError as exc:
            self.connected = False
            raise InfrastructureError(str(exc))

    def listen_feedback(self, timeout, namespace=None):
        """
        Listen to output and log as feedback
        Returns the number of characters read.
        """
        index = 0
        if not self.raw_connection:
            # connection has already been closed.
            return index
        if timeout < 0:
            raise LAVABug("Invalid timeout value passed to listen_feedback()")
        try:
            self.raw_connection.logfile.is_feedback = True
            self.raw_connection.logfile.namespace = namespace
            index = self.raw_connection.expect(
                [".+", pexpect.EOF, pexpect.TIMEOUT], timeout=timeout
            )
        finally:
            self.raw_connection.logfile.is_feedback = False
            self.raw_connection.logfile.namespace = None

        if index == 0:
            return len(self.raw_connection.after)
        return 0
