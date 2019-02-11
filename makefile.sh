#!/bin/bash
# todo: Should we re-write in python so it will be cross-platform?

export SKIP_GENERATE_AUTHORS=1
export SKIP_WRITE_GIT_CHANGELOG=1

if [ $1 == 'devpi' ]; then

    export USER=$1
    # todo: Get from optional user input
    export INDEX=dev
    export PASSWORD=123

    # todo: Test if already logged in.
    devpi use $PIPENV_PYPI_MIRROR/$USER/$INDEX
    devpi login $USER --password $PASSWORD
    devpi upload
else
    python setup.py sdist
fi