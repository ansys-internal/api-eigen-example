.. _getting_started:

***************
Getting started
***************

The API Eigen example package is a simple project for showing PyAnsys
users and developers the differences between the API REST communication protocol
and the gRPC communication protocol that is used extensively in PyAnsys libraries.

This project has multiple language implementations.

================================
API Eigen Example Python project
================================

To use the API Eigen Example project in its Python version, you do not need any specific requirements or
additional software, apart from the ones that are installed via the requirements ``--all-files``
and a CMake version of the Eigen library. 

------------
Installation
------------

First install the Eigen library (and CMake if it is not present). For Ubuntu distributions, it is as
easy as running:

.. code:: bash

    sudo apt install cmake libeigen3-dev

To install a local version of the API Eigen Example project, clone the `repository <https://github.com/ansys/api-eigen-example>`_
through the Ansys GitHub Enterprise account:

.. code:: bash

	git clone https://github.com/ansys/api-eigen-example.git

.. note:
    Other Ansys Python packages are available through the Ansys GitHub Enterprise account or
    through `PyPI <https://www.pypi.org>`_. 

If you want to use Python versions of the API Eigen Example project, install the
demo-eigen-wrapper, which is a wrapper to the Eigen library that uses pybind11:

.. code:: bash

    pip install -r requirements/requirements_eigen_wrapper.txt ./src/ansys/eigen/cpp/eigen-wrapper

Finally, install the project with:

.. code:: bash

    pip install -r requirements/requirements_build.txt .

---------------------------
Starting to use the project
---------------------------

Once the API Eigen Example project has been installed, start to make use of the Python
packages by importing them:

.. code:: python

    >>> import ansys.eigen.python.rest.server as rest_server
    >>> import ansys.eigen.python.rest.client as rest_client
    >>> client = rest_client.DemoRESTClient("127.0.0.1", 5000)
    >>> client.get_connection_details()

For more examples, see the :ref:`user_guide`.


=============================
API Eigen Example C++ project
=============================

------------
Installation
------------

To use the API Eigen Example C++ projects, the installation process is a bit more cumbersome.
First install the packaged library ``cmake``:

.. code:: bash

    sudo apt install cmake


Depending on the C++ project, dependencies vary. Go to your sections of interest from those that follow.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ REST Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ REST server manually is a simple process. Run the following commands from
the root of the repository:

.. code:: bash

    pip install -r requirements/requirements_build.txt .
    cd src/ansys/eigen/cpp/rest/server/build/
    conan install .. && cmake .. && cmake --build . && sudo make install


Once dependencies are installed, you can use the C++ REST server. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

.. code:: cpp

    #include <apieigen/rest/RestServer.hpp>

    int main() {
       // Let us instantiate our server
       ansys::rest::server::RestServer server{};

       // Start serving!
       server.serve();
    }


For compiling, link the library with:

.. code:: bash

    g++ -o myServer main.cpp -lapieigen_example_rest_server


You can run your server with:

.. code:: bash

    ./myServer


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ REST Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ REST client manually is a bit more complex. You must install some
development libraries and compile in place some additional external libraries.

First, install a ``dev`` version of ``libcurl``. Using the Ubuntu package manager ``apt``, you can run:

.. code:: bash

    sudo apt install libcurl4-openssl-dev

Once ``libcurl-dev`` is installed, you must compile some external projects. These external projects have
been frozen at a given version within this repository. You can find them in the ``external`` folder.

To install them, run these commands:

.. code:: bash

    sudo apt update && sudo apt install libcurl4-openssl-dev && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && sudo make install && cd -
    sudo apt update && cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && sudo make install && cd - 


Once dependencies are installed, you can build and install the client library with:

.. code:: bash

    cd src/ansys/eigen/cpp/rest/client/build/ && cmake .. && cmake --build . && sudo make install && cd -


You can use the REST C++ Client library. Start writing your own C++ ``client.cpp`` file and
include the project header files as follows:

.. code:: cpp

   #include <vector>
   #include <apieigen/rest/EigenClient.hpp>

   int main(int argc, char const *argv[]) {
       // ------------------------------------------------------------------------
       // Deploying the client
       // ------------------------------------------------------------------------
       // Instantiate an EigenClient
       auto client = ansys::rest::client::EigenClient("http://0.0.0.0:18080");

       // ------------------------------------------------------------------------
       // REQUESTING GREETING - A.K.A "Hello World"
       // ------------------------------------------------------------------------
       // Let us request a greeting!
       client.request_greeting();

       // Exit successfully
       return 0;
   }


For compiling, link the library as follows:

.. code:: bash

    g++ -o myClientApp client.cpp -lapieigen_example_rest_client


You can run your client app with:

.. code:: bash

    ./myClientApp

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ gRPC Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ gRPC server manually is a simple process. To use the `conan <https://conan.io/>`_ package manager
to install dependencies, run the following command lines from the root of the repository:

.. code:: bash

    cd src/ansys/eigen/cpp/grpc/server/
    make compile && make install && ./deploy_dependencies.sh


You might need to run the previous ``install`` and ``deploy`` commands with root privileges.

Once dependencies are installed, you can use the C++ gRPC server. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

.. code:: cpp

    #include <apieigen/grpc/GRPCServer.hpp>

    int main() {
       // Let us instantiate our server
       ansys::grpc::server::GRPCServer server{};

       // Start serving!
       server.serve();
    }


For compiling, link the library as follows:

.. code:: bash

    g++ -o myServer main.cpp -lapi_eigen_example_grpc_server

You can run your server with:

.. code:: bash

    ./myServer


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ gRPC Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ gRPC client manually is a simple process. To use the `conan <https://conan.io/>`_
package manager to install dependencies, run the following commands from the root of the repository:

.. code:: bash

    cd src/ansys/eigen/cpp/grpc/client/
    make compile && make install && ./deploy_dependencies.sh


You might need to run the previous ``install`` and ``deploy`` commands with root privileges.

Once dependencies are installed, you can use the C++ gRPC client. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

.. code:: cpp

    #include <vector>
    #include <apieigen/grpc/GRPCClient.hpp>

    int main() {
        // ------------------------------------------------------------------------
        // Deploying the client
        // ------------------------------------------------------------------------
        // Instantiate a GRPCClient
        ansys::grpc::client::GRPCClient client{"0.0.0.0", 50000};

        // ------------------------------------------------------------------------
        // REQUESTING GREETING - A.K.A "Hello World"
        // ------------------------------------------------------------------------
        // Let us request a greeting!
        client.request_greeting("Michael");

        // ------------------------------------------------------------------------
        // Performing vector operations
        // ------------------------------------------------------------------------
        // Let us create some reference vectors
        std::vector<double> vec1{1.0, 2.0, 3.0, 50.0};
        std::vector<double> vec2{4.0, 5.0, 8.0, 10.0};

        // Let us add them
        auto result = client.add_vectors(vec1, vec2);

        // Exit successfully
        return 0;
    }


For compiling, link the library as follows:

.. code:: bash

    g++ -o myClientApp main.cpp -lapi_eigen_example_grpc_client


You can run your client with:

.. code:: bash

    ./myClientApp

