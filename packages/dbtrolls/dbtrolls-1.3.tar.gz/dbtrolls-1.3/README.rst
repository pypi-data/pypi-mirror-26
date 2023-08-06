.. image:: https://raw.githubusercontent.com/caputomarcos/dbtrolls/master/dbtrolls.png



dbtrolls
========


A simple tool to make Dev's life happy.

License
-------
Licensed under the GNU General Public License (GPL).


Install
-------

Follow the steps below to get everything up and running.


pip
---

Package Index > dbtrolls > 1.1 pip_.

.. _pip: https://pypi.python.org/pypi/dbtrolls

1. Create project folder:

   .. code-block:: bash

        $ mkdir dbtrolls && cd dbtrolls

2. Create virtualenv in the normal way:

   .. code-block:: bash

        $ virtualenv env --python=python

3. Active your new virtualenv:

   .. code-block:: bash

        $ source env/bin/activate


4. Install dbtrolls:

   .. code-block:: bash

        $ pip install dbtrolls


Git
----

1. Clone repository:

   .. code-block:: bash

        $ git clone git@github.com:caputomarcos/dbtrolls.git

2. Go to dbtrolls source folder:

   .. code-block:: bash

        $ cd dbtrolls/

3. Create virtualenv in the normal way:

   .. code-block:: bash

        $ virtualenv env --python=python

4. Active your new virtualenv:

   .. code-block:: bash

        $ source env/bin/activate


5. Create dev environment:

   .. code-block:: bash

        $ make develop


Usage
------

1. Create config file:

   .. code-block:: bash

        $ dbtrolls -c --database_source=<DATABASE_SOURCE> --database_target=<DATABASE_TARGET>

2. Execute a single SQL file:

   .. code-block:: bash

        $ dbtrolls -s <SQL_FILE> --fix --preload

3. Execute a collection of SQL files:

   .. code-block:: bash

        $ dbtrolls -m
