## eLxr Certification Testing
This package provides certification testing for eLxr.

## How it works

### Directory Structure
The directory structure (when run) looks like this:

.
├── dist
│   ├── elxr_validator-0.1.0-py3-none-any.whl
│   └── elxr_validator-0.1.0.tar.gz
├── Dockerfile
├── elxr_validator
│   ├── bin
│   ├── device.yaml
│   ├── inline
│   ├── job.yaml
│   ├── lava
│   ├── lib
│   ├── src
│   └── utils
├── poetry.toml
├── pyproject.toml
├── README.md
└── run.sh

## How it works
The run.sh script first runs docker, through which the dependencies whl file
under dist is created. The run.sh script then installs the dependencies file,
and then runs the following command:

[elxr $] python src/main.py

from the elxr_validator directory.

The test definitions are present in the file elxr_validator/job.yaml.