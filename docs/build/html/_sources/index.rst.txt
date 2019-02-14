BBTest - black box testing
==========================

BBTest is a python based automation framework for black box testing. Tests are
executed in a virtual lab, supporting multiple Hosts and the network 
connecting them.

Our runner is based on `pytest <http://docs.pytest.org>`_ so we can use its
switches, markers, switchs and plugins.  Here's a shot list of our favorite 
switches:

.. code-block:: console

    -k <regex>         only run classes & methods that match the regex
    --lf               only run the last failure
    --pdb              start the debugger on errors
    -m <markerex>      only run test matching given marker expression

We've extended pytest to include our own params:

.. code-block:: console

    --pip-index <url>  url of python package index to use
    --ep-ip <ip>       ip address of the endpoint to run tests one
    --ep-os            win|linux|mac

.. note:: --ep-os will be removed in version 0.3

.. toctree::
   :maxdepth: 2
   :glob:

   installation
   API


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
