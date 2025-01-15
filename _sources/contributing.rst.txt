.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar with
it and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_ before attempting to
contribute to the API Eigen Example repository.
 
The following contribution information is specific to the API Eigen Example repository.

Cloning the API Eigen Example Repository
----------------------------------------
Run this code to clone and install the latest version of the repository in development
mode:

.. code::

    git clone https://github.com/ansys/api-eigen-example.git
    cd api-eigen-example
    pip install -r requirements/requirements_eigen_wrapper.txt ./python/eigen-wrapper
    pip install -r requirements/requirements_build.txt .

Building documentation
----------------------
To build the documentation locally you need to follow these steps at the root
directory of the repository:

.. code:: 

    pip install -r requirements_docs.txt
    cd doc
    make html

After the build completes, the HTML documentation is located in the
``_builds/html`` directory. You can load the ``index.html`` into a web
browser. To clear the documentation directory, you can run:

.. code::

    make clean

Posting issues
--------------
Use the `API Eigen Example Issues <https://github.com/ansys/api-eigen-example/issues>`_ page to
submit questions, report bugs, and request new features.


Code style
----------
API Eigen Examples is compliant with the `PyAnsys Development Code Style Guide
<https://dev.docs.pyansys.com/coding_style/index.html>`_.  Code style is checked
by making use of `pre-commit <https://pre-commit.com/>`_. Install this tool and
activate it with:

.. code::

   python -m pip install pre-commit
   pre-commit install

Then, you can make use of the available configuration file ``.pre-commit-config.yml``,
which is automatically detected by pre-commit:

.. code::

   pre-commit run --all-files --show-diff-on-failure

