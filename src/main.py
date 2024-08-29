import os
import sys
import logging

logger = logging.getLogger()

logger.debug("Start Validation Program")

# Add lava to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../lava"))

from windriver.cli.elxr import Validator

def main():
    validator = Validator()
    validator.validate('job.yaml')

main()

logger.debug("End Validation Program")
