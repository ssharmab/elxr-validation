import os
import sys
import logging
import uuid
import yaml
import re
from prettytable import PrettyTable # type: ignore

# Add lava to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../lava"))

from lava_common.yaml import yaml_safe_load
from lava_common.log import YAMLLogger
from lava_dispatcher.device import NewDevice
from lava_dispatcher.parser import JobParser
from lava_dispatcher.job import Job

logging.setLoggerClass(YAMLLogger)
logging.basicConfig(level=logging.DEBUG)

class ResultsFilter(logging.Filter):
    """
    A log filter which only returns lava results
    """
    def filter(self, record):
        msg = yaml_safe_load(record.msg)
        return msg['lvl'] == "results"

class ResultsHandler(logging.Handler):
    """
    A results log handler which takes lava test results and appends them to a results array
    """
    def __init__(self, level=logging.INFO, results = []):
        super().__init__(level)
        self._results = results
        self.addFilter(ResultsFilter(__file__))

    def emit(self, record):
        record_msg = yaml_safe_load(record.msg)
        result = record_msg['msg']
        self._results.append(result)

class Validator:
    """
    The eLxr Validator
    """
    def __init__(self):
        self._results = []
        
        results_handler = ResultsHandler(results = self._results)
        self._logger = logging.getLogger("dispatcher")
        self._logger.addHandler(results_handler)
        
    def validate(self, job_path, device_path):
        job_definition = open(job_path, 'r').read()
        device = NewDevice(device_path)
        parser = JobParser()

        job : Job =  parser.parse(
            job_definition,
            device,
            str(uuid.uuid4())[:8],
            logger=self._logger,
            dispatcher_config=None,
            env_dut=None,
        )
        
        job.validate()
        job.run()
        print(yaml.dump(self._results))
        table = PrettyTable()
        summary = PrettyTable()
        table.field_names = ['Definition','Case','result','starttc','endtc']
        summary.field_names = ['Definition','Case','result','duration']
        
        for element in self._results:
            if re.match(r"(\d+)_*",element['case']):
                summary.add_row([element['case'],element['definition'],element['result'],element['duration']])
        print(summary)
                
        for element in self._results:
            if element['definition'] != 'lava':
                table.add_row([element['case'],element['definition'],element['result'],element['starttc'],element['endtc']])
            
        print(table)
        print(self._results)
        if all(map(lambda x : x['result'] == 'pass', self._results)):
            print("SUCCESSFULLY VALIDATED")

validator = Validator()
validator.validate('job.yaml', "device.yaml")
