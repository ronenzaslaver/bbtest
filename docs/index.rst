BBTest - black box testing
==========================

BBTest automation framework for black box testing in a virtual lab. The lab
supports multiple Hosts & OSs and well as flexible network. 

Our test case class inherits from :class:`unittest.TestCase`,
so you use `setUp` and `destroy` and `test*` methods.
To run the tests you can use your favorite python tests runner (ours is
pytest).

.. automodule:: bbtest.testcases
    :members:
    :undoc-members:
    :show-inheritance:

The Black Box
-------------

.. automodule:: bbtest.blackboxes
    :members:

The Lab
-------

.. automodule:: bbtest.labs
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: bbtest.hosts
    :members:
    :undoc-members:
    :show-inheritance:



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
