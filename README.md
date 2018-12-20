BBTest - TestCase based black box testing and lab
=================================================

BBTest automation framework for black box testing and a virtual lab. The lab supports multiple Hosts & OSs and well as flexible network. 

The test cases themselvs are written using `bbtest.BBTestCase` as a base class.  Inherits from TestCase, so we use `setup` and `destroy` and `test*` methods.
To run the tests you can use your favorite python tests runner (ours is pytest).

We've added a class property `LAB` that holds a dictionary defining the lab enviornment.

Installation
------------

After forking and cloning this repo, open a shell in this folder:

```bash

$ pipenv shell
$ PYTHONPATH=. pytest
```

Documentation
-------------

We are using Sphinx to publish our documentation. To generate and serve the documentation:

```bash

$ pipenv install -d
$ cd docs
$ make html
$ cd _build/html
$ python -m http.server


