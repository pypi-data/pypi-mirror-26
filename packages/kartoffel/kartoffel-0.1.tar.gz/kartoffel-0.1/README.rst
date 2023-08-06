Identify modules used in a Python application.

To run::

    kartoffel module:func [args for application]

For example, for IPython::

    kartoffel IPython:start_ipython

Your application will run. If any modules are dynamically loaded (e.g. plugins),
activate the features to ensure that they are loaded. Then quit your application.

After your application exits, Kartoffel will capture a list of all the Python
modules loaded (``sys.modules``). Then it will classify these into groups:

- Modules from identified distributions (i.e. PyPI packages)
- Modules from the standard library (using `stdlib_list <http://python-stdlib-list.readthedocs.io/>`_)
- Modules not from files (builtins and dynamically created modules)
- Unidentified

The results are saved as ``kartoffel-result.json`` in the working directory.
A summary is printed on stdout.
