BBTest - TestCase based black box testing and lab
=================================================

BBTest automation framework for black box testing and a virtual lab. The lab supports multiple Hosts & OSs and well as flexible network. 

The test cases themselvs are written using `bbtest.BBTestCase` as a base class.  Inherits from TestCase, so we use `setup` and `destroy` and `test*` methods.
To run the tests you can use your favorite python tests runner (ours is pytest).

We've added a class property `LAB` that holds a dictionary defining the lab enviornment.

# Contributing

## Prerequisites
- Install Python 3.7.2
- Install pipenv under Python 3.7.2 - ```$ pip install pipenv```
- If you use Git Bash on Windows, we recommend using the [.bashrc](installations/.bashrc) sample
to make sure prompts are displayed properly. Don't forget to:```bash $ source ~/.bashrc```

## Install runner
First fork and clone this repo.  Then use `pipenv` to setup the python environment.
Open a shell in the cloned repo folder and type:

```bash
$ pipenv --python 3.7
$ pipenv shell
$ pipenv install
$ pipenv install --dev
```

Make sure Python interpreter points to pipenv on your IDE.

For PyCharm users, Pycharm should auto detect pipenv (from Pycharm version 2018.2 and above).

Note: If Pipenv Environment is missing, make sure your Pycharm version supports pipenv.

If Pycharm not auto detecting, please add manually the following:

Go to File --> Settings --> Project Interpreter --> Click on Setting (top right, wheel icon)
--> Add --> Choose Pipenv Environment --> In Pipenv executable, point to pipenv.exe.
Default path: C:\Python37\Scripts\pipenv.exe



To run tests on local machine simply run
```bash
$ pytest tests --os=local
```
## Install remote host
To turn a remote machine into a bbtest host you will need to install an FTP server and RPyC server on the machine.
You can find some tips on FTP and Python installations in the [INSTALLATIONS.md](installations/README.md) file.
- Start FTP server on the remote machine with root directory set to "temp" directory (c:\temp, /tmp).
- Make sure python2 and python3 are recognized as short to Python 2 and Python 3 respectively 

Once FTP and Python 3.7 are installed, download and start python RPyC server:
```bash
$ pip3 install -i http://cyber-devpi.cyberdomain.local/root/cr --trusted-host cyber-devpi.cyberdomain.local bbtest
$ bbhost --host 0.0.0.0
```

Now it's time to install bbtest package and run tests. When you run tests, bbtest runner will need to update bbtest
package on the remote host. This is done as part of the host installation process as part of the test class setup
process. The update is performed using "pip install -U bbtest" and the user can set a pypi index to get bbtest package
from or install from local package.

### Install from pypi
If you select to use pypi server you need to upload the new bbtest package to the server. We recommend to use
[devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html) server to mirror PyPi and store bbtest package amd
devpi package is installed as part of bbtest pipenv.

On the runner machine:
- Install devpi
```bash
$ pip install devpi
```

- Create user on devpi server:
Cybereason pypi server is "cyber-devpi.cyberdomain.local".

Note: Sometimes the devpi command fails (fail to login, fail to use, etc.) in Windows Git Bash. If this happens, try 
running the commands in native Windows CMD.
```bash
$ devpi use http://<devpi server>/
$ devpi user -c <your name> password=<your password>
$ devpi login <your name> <your password>
$ devpi index -c dev bases=root/pypi
$ devpi use http://<devpi server>/<your name>/dev
```

- Upload
```bash
$ cd <bbtest project root folder>
$ devpi upload
```
The upload command creates bbtest package under  dist/ folder (e.g. dist/bbtest-0.0.1.dev191.zip) and uploads the
package to devpi server under "http://<devpi_server>/<your_name>/dev" index.

Note: The build above uses a `requirments.txt` file which need to be updated every time a new package is added. Just run
`pipenv lock -r > requirments.txt` and don't forget to commit the change.

Set the full path to this index as the pypi parameter to pyest
```bash
$ pytest tests --pip-index="-i http://<devpi server>/<your name>/dev --trusted-host <devpi server>" --<other remote host parames>
```

### Install from local package
Note: If you select to install from pypi, you should skip this step.
 
If you select to install from local package you need to create new bbtest package on the runner machine
```bash
$ cd <bbtest project root folder>
$ python setup.py sdist
```
A new package will be created under dist/ folder (e.g. dist/bbtest-0.0.1.dev191.tar.gz).

Set the full path to this file as the pypi parameter to pyest
```bash
$ pytest --pypi=<full path to bbtest package> --<other remote host params, see below>
```

## Run tests
Now you can run tests on the remote host:
```bash
$ pytest --os (win|linux) --ip <IP> [--user <USER> --pw <PASSWORD>] --pypi=<see above>
```

# Examples
The `examples` folder  contain tutorials and how-tos demoing parts of bbtest. You are 
welcome to browse the
[docs](https://daonb.github.io/bbtest/build/html/examples.html).  
If you want to play with the framework,  run `ipython` and you'll get an env 
where you can simply `import bbtest`.

Documentation
-------------

We are using Sphinx to publish our documentation. To generate and serve the documentation:

```bash
$ pipenv shell
$ cd docs
$ make html
$ cd _build/html
$ python -m http.server
```
