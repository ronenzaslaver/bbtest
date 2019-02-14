Installation
============

Prerequisites
-------------

* Install Python 3.7.2
* Install pipenv under Python 3.7.2 - ``$ pip install pipenv``
* If you use Git Bash on Windowsi and your prompts are funny, try coping
  ``installations/bashrc`` to the end of your .bashrc and ``source ~/.bashrc``

Get the Code and dependencies
-----------------------------

First fork our testing suite from
`<https://github.com/cybereason-labs/probe-tests>`_ and then:

.. code-block:: console

    $ git clone git@github.com:<your github username>/probe-tests.git
    $ cd probe-tests
    $ pipenv install
    $ pipenv install --dev
    $ pipenv shell


IDE Configuration
---------------------

Feel free to use your prefered development enviornment.
For now, we only include instructions for the PyCharm IDE so if you're using 
a diffrent IDE please configure it to integrate with ``pipenv`` and add document
it below.

Pycharm should auto detect pipenv (from Pycharm version 2018.2 and above).  If
Pycharm not auto detecting, please add manually the following:

Go to File --> Settings --> Project Interpreter --> Click on Setting (top right, wheel icon)
--> Add --> Choose Pipenv Environment --> In Pipenv executable, point to pipenv.exe.
Default path: C:\Python37\Scripts\pipenv.exe

.. note:: If Pipenv Environment is missing, make sure your Pycharm version
   supports pipenv.


To run tests on local machine simply run ``pytest``

Install a Slave
---------------

Our runner can do all its work on the local machine, but the major benefits
are only there when using remote slave hosts. To make a host into a slave, 
we need Python 3.7 installed and in case you have a firewall, port 57911
to be open.  To Install Python 3.7.2:

* For debian based distros (like Ubuntu) use:

.. code-block:: console

    $ add-apt-repository ppa:deadsnakes/ppa
    $ apt-get update
    $ apt install python3.7 python3.7-dev python3-pip

* For CentOS you will need to build Python from the source:

.. code-block:: console

    $ yum install -y epel-release  centos-release-scl gcc openssl-devel
    $ yum install -y libffi-devel bzip2-devel
    $ cd /tmp
    $ wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
    $ tar xzf Python-3.7.2.tgz
    $ cd Python-3.7.2/
    $ ./configure --enable-optimizations
    $ make
    $ make install

* For OSX:

.. code-block:: console

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    $ brew install python3

.. note: after copying files to the target host machine you might need
to convert the files from dos to unix format, if this is the case install and
run dos2unis util.

Now you are ready to install the bbtest package and run it as a host:

.. code-block:: console

    $ /usr/bin/python3.7 -m pip install -UI -i http://172.16.57.40/root/cr --trusted-host 172.16.57.40 bbtest
    $ bbhost --host 0.0.0.0

Run Tests
---------

Now it's time to get back to the runner and run the tests using the slave:

.. code-block:: console

    $ pytest --ep-os (win|linux|mac) --ep-ip <IP> --pypi-index http://172.16.57.40/root/cr
