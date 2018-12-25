ToDo
====
Based on a tip from Roy, our first example is a to-do component copied from
`ToDo.txt <http://todotxt.org/>`_ . In the example's code we show how we wrapped it
as a black box and then use it to test the ToDo's interface.


.. code-block:: bash

  $ examples/todo/src/todo.sh -h

  Usage: todo.sh [-fhpantvV] [-d todo_config] action [task_number] [task_description]

  Actions:

    add|a "THING I NEED TO DO +project @context"
    addm "THINGS I NEED TO DO
       MORE THINGS I NEED TO DO"
    addto DEST "TEXT TO ADD"
    append|app ITEM# "TEXT TO APPEND"
    archive
    command [ACTIONS]
    deduplicate
    del|rm ITEM# [TERM]
    depri|dp ITEM#[, ITEM#, ITEM#, ...]
    do ITEM#[, ITEM#, ITEM#, ...]
    help [ACTION...]
    list|ls [TERM...]
    listall|lsa [TERM...]
    listaddons
    listcon|lsc [TERM...]
    listfile|lf [SRC [TERM...]]
    listpri|lsp [PRIORITIES] [TERM...]
    listproj|lsprj [TERM...]
    move|mv ITEM# DEST [SRC]
    prepend|prep ITEM# "TEXT TO PREPEND"
    pri|p ITEM# PRIORITY
    replace ITEM# "UPDATED TODO"
    report
    shorthelp

  ...

To test this component we need to first code a class based on :class:`bbtest.blackboxes.BlackBox` that install,
removes and runs the script.

.. autoclass:: examples.todo.tests.todo_box.ToDoBox
    :members:
    :undoc-members:
    :show-inheritance:

Using this component, we code a test suite :
 
.. literalinclude:: /../examples/todo/tests/test_suite.py
