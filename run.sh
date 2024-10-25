#! /bin/bash
###############################################################
##
##
###############################################################

DOCKER=docker
PYTHON=python3
PIP=pip3
DOCKER_IMAGE="elxr-validator"
DEPENDENCIES_WHEEL="dist/elxr_validator-0.1.0-py3-none-any.whl"
DEPENDENCIES_BUILD_CMD="poetry build"

# usage notes
usage() {
    cat << USAGE
 This script executes eLxr certification tests. The script
 assumes that docker and python3 are supported on the platform.

 Usage:
 [elxr $] ./run.sh
USAGE
}

# create dependencies
create_dependencies() {
    echo "-------------------------------------------"
    echo "Building image"
    rc=$(${DOCKER} build -t ${DOCKER_IMAGE} .)

    echo "-------------------------------------------"
    echo "Creating dependencies"
    rc=$(${DOCKER} run -ti -v ${PWD}:/workspaces/${DOCKER_IMAGE} ${DOCKER_IMAGE} /bin/bash -c "${DEPENDENCIES_BUILD_CMD}")

    if [[ ! -e dist ]]; then
        echo "Dependencies not created: ${rc}"
        exit -1
    fi
}

# install dependencies
install_dependencies() {
    echo "Installing...."
    rc=$(${PIP} install ${DEPENDENCIES_WHEEL})
    if [[ ${rc} -ne 0 ]]; then
        echo "Unable to install dependencies: ${rc}"
    fi
}

# run the tests on the host and not in the container
run_tests() {
    echo "Running tests"
    pushd elxr_validator
    rc=$({PYTHON} src/main.py 2>&1)
    echo "Tests DONE with ${rc}"
    popd
}

create_dependencies
install_dependencies
run_tests