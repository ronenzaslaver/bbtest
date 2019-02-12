#!/bin/bash
# todo: Should we re-write in python so it will be cross-platform?

export SKIP_GENERATE_AUTHORS=1
export SKIP_WRITE_GIT_CHANGELOG=1

if [ $1 == '--help' ]; then
    echo "Usage: $0 <user> <password>"
    exit 0
fi

USER=$1
PASSWORD=$2

devpi use $PIPENV_PYPI_MIRRO
devpi login $USER --password $PASSWORD
devpi upload
