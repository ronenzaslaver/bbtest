#!/bin/bash
# todo: Should we re-write in python so it will be cross-platform?

export USER=$1
# todo: Get from optional user input
export INDEX=dev
export PASSWORD=123

# todo: Test if already logged in.
devpi use $PIPENV_PYPI_MIRROR/$USER/$INDEX
devpi login $USER --password $PASSWORD
devpi upload
