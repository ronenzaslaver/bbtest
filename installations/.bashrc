#
# Basic Git bash configuration to work in virtualenv environment.
#
# Native Linux bash supports these configurations by default.
#

alias ll='ls -l'

# run all CLI commands with winpty
alias python='winpty --mouse python.exe'
alias ipython='winpty --mouse ipython.exe'
alias devpi='winpty --mouse devpi.exe'
alias ftp='winpty --mouse ftp'

# Get Virtual Env
if [[ $VIRTUAL_ENV != "" ]]
    then
      # Strip out the path and just leave the env name
      venv="(${VIRTUAL_ENV##*\\}) "
else
      # In case you don't have one activated
      venv=''
fi

# List of basic colors for the prompt, you can set your own color of-course.

red=$'\[\033[0;31m\]'
green=$'\[\033[01;32m\]'
yellow=$'\[\033[01;33m\]'
purple=$'\[\033[01;34m\]'
pink=$'\[\033[01;35m\]'
blue=$'\[\033[01;36m\]'
white=$'\[\033[01;37m\]'

# Add venv to prompt
export PS1=${green}'${venv}'${blue}'$(pwd)$ '${white}
