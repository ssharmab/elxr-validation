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
        job.run()

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
