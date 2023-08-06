===============================
instance-config
===============================

.. image:: https://img.shields.io/pypi/v/instance-config.svg
    :target: https://pypi.python.org/pypi/instance-config

A simple library using consul locks to do one-time configuration tasks on AWS instances.

How to use it
--------------

.. code-block:: python

    from instance_config import Instance

    instance = Instance()

    @instance.every()
    def do_each_time():
        # This will run every time the script is invoked.
        return

    @instance.once(key='locks/my_app/create_user', version=1, timeout=60)
    def create_user():
        # This will only be run once, in declared order, for each version.
        return do_create_user()




History
-------

0.1.2 (2017-11-06)
++++++++++++++++++

* First release on PyPI.


