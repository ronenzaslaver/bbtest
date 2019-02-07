BBTest - TestCase based black box testing and lab
=================================================

BBTest automation framework for black box testing and a virtual lab. The lab supports multiple Hosts & OSs and well as flexible network. 

The test cases themselvs are written using `bbtest.BBTestCase` as a base class.  Inherits from TestCase, so we use `setup` and `destroy` and `test*` methods.
To run the tests you can use your favorite python tests runner (ours is pytest).

We've added a class property `LAB` that holds a dictionary defining the lab enviornment.

# Contributing

First fork and clone this repo.  Then use `pipenv` to setup the python environment.
Open a shell in the cloned repo folder and type:

```bash
$ pipenv --python 3.7
$ pipenv shell
$ pipenv install --dev
```
Then take a look at pytest custom options and run tests: 
```bash
$ pytest --help
$ pytest [custom options] tests
```
To run tests on local machine simply run
```bash
$ pytest tests
```
## Remote hosts
To run tests on remote machines you'll need a [devpi] server to mirror PyPi
and an FTP server and RPyC server on remote machine. You can find some tips on FTP and Python installations in the
[INSTALLATIONS.md](installations/README.md) file. 

- Download and install python 3.7 and RPyC:
```bash
$ pip3 install rpyc
$ rpyc_classic.py --host 0.0.0.0
```
- Start FTP server on the remote machine with root directory set to "temp" directory (c:\temp, /tmp).
- Now you can run tests on the remote host:

```bash
$ devpi upload
$ pytest --os (win|linux) --ip <IP> [--user <USER> --pw <PASSWORD>]
```

The build above uses a `requirments.txt` file which need to be updated every
time a new package is added. Just run `pipenv lock -r > requirments.txt` and 
don't forget to commit the change.

## Working with devpi
- Register and login:
```bash
devpi use http://cyber-devpi.cyberdomain.local/
devpi user -c YOURNAMEv
devpi login YOURNAME
devpi index -c dev bases=root/pypi
devpi use http://cyber-devpi.cyberdomain.local/YOURNAME/dev
```
- Upload
```bash
devpi upload
```
Now you can find your new package under YOURNAME/dev
- Download
Go to the destination host and run:
```bash
python -m pip install -UI -i http://172.16.57.40/YOURNAME/dev --trusted-host 172.16.57.40 bbtest
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
