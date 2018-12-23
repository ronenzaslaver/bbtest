Test a simple Installer
=======================
In this example we will test an installer that gets a server url and installs
a script that POSTs to the server. We run the installer with the url of a stub
server, test the script was created, run the script, and check the server
logs for the registration message. The code used in this sample can be found
under `/examples/todo`.

Our lab is made from two boxes running on two hosts: `client` and `server`.
The client host runs a :class:`bbtest.blackboxes.HomeBox` which is simple box
that creates a temporary folder on install and store it in `self.path`.
On clean - which happens before every test method - it removes all the files
from home and on unistall, removes the dir.

For a server we use :class:`bbtest.blackboxes.SpyServerBox` that logs all 
POSTed messages so we can assert a message was recieved. 

.. note:: 
    It's possible to run both boxes on a single host and simplify the suite

.. literalinclude:: /../examples/installer/tests/test_suite.py

.. literalinclude:: /../examples/installer/installer.sh

