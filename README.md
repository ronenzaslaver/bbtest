BBTest - TestCase based black box testing and lab
=================================================

BBTest automation framework for black box testing and a virtual lab. The lab supports multiple Hosts & OSs and well as flexible network. 

The test cases themselvs are written using `bbtest.BBTestCase` as a base class.  Inherits from TestCase, so we use `setup` and `destroy` and `test*` methods.
To run the tests you can use your favorite python tests runner (ours is pytest).

We've added a class property `LAB` that holds a dictionary defining the lab enviornment.

Installation
------------

Fork and clone this repo.

Testing
-------
In order to run all tests, you beed to have python environment with all packages installed and RPyC server running.
Open a shell in the cloned repo folder:

```bash
$ pipenv shell
$ rpyc_classic.py &
$ pytest
```

The examples contain tutorials and how-tos demoing parts of bbtest. You are 
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
