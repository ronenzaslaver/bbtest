# todo: Should we re-write in python so it will be cross-platform?

# todo: Get from mandatory user input
export USER=yoram
# todo: Get from optional user input
export INDEX=dev
export PASSWORD=123

# todo: Test if already logged in.
devpi use $PIPENV_PYPI_MIRROR/$USER/$INDEX
devpi login $USER --password $PASSWORD
devpi upload
