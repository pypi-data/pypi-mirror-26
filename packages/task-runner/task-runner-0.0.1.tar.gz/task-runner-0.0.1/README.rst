task-runner
===========

taskrunner runs your methods until they stop failing.

Motivation
----------

taskrunner is a crude way to force your methods to complete. This is
particularly useful when functions can be expected to throw exceptions
but shouldn’t stop execution. Effectively, taskrunner catches all
exceptions and makes sure that the result is not in a list of excluded
return values.

Installation
------------

taskrunner is available via pip:

::

    $ pip install taskrunner

Usage
-----

.. code:: python

    from taskrunner import TaskRunner

    def some_function_that_may_throw(some_argument, another_argument):
        # Do something

    task_runner = TaskRunner()
    result = task_runner.run_until_complete(target=some_function_that_may_throw, args=('123','456'))
    print(result) # Hopefully something useful