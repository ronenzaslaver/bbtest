Contributing
============

We welcome contributors who want to extend or fix BBTest.
First fork BBTest from
`<https://github.com/cybereason-labs/bbtest>`_ and then:

.. code-block:: console

    $ git clone git@github.com:<your github username>/bbtest.git
    $ cd bbtest
    $ pipenv install
    $ pipenv install --dev
    $ pipenv shell
    $ pytest

To test your code you will need to create and use your own pypi index:

.. code-block:: console

    $ devpi use http://172.16.57.40
    $ devpi user -c <your username> password=<your password>
    $ devpi login <your username> <your password>
    $ devpi index -c dev bases=root/cr
    $ devpi use <your name>/dev

.. note:: In Windows Git Bash, ``devpi`` sometimes fails (fail to login, fail
   to use, etc.) If this happens, try running the commands in native Windows
   CMD.

If you're unlucky and find yourself working on mutiple issues at the same time,
you can create as many indexes as you want using: ``devpi index -c <branch name>
bases=root/cr``.

Once you've coded and tested your changes you need to upload them to your index:

.. code-block:: console

    $ devpi upload

The upload command creates a BBTest package under  dist/ folder (e.g.
dist/bbtest-0.0.1.dev191.zip) and uploads the package to devpi server under
"http://172.16.57.40/<your_name>/dev" index.

.. note:: The build above uses a ``requirments.txt`` file which need to be
   updated every time a new package is added. Just run ``pipenv lock -r >
   requirments.txt`` and don't forget to commit the change.

To run you tests using your own version of Python go back to ``probe-tests``
home and use ``--pip-index`` switch to point bbtest at your index:

.. code-block:: console

    $ pytest --pip-index=http://172.16.57.40/<your username>/dev

Pipenv Integration
------------------

To get pipenv to use your index when installing packages:

.. code-block:: console

    $ export PIPENV_PYPI_MIRROR=http://172.16.57.40/benny/dev

We found it usefull to add the export command to the bashrc.

Documentation
-------------

Our docs are located under the ``docs`` directory. We use Sphinx to extract 
documentation from the code and publish it as html (or latex if you need it).\
To generate and serve the documentation:

.. code-block:: console

    $ pipenv shell
    $ cd docs
    $ make html
    $ python -m http.server -d build/html


