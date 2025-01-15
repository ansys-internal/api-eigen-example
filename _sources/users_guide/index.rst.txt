
.. _user_guide:

************
User's guide
************
This guide describes how to use the API Eigen Example package and its modules
and components.

=================================================
Understanding the API Eigen Example Python module
=================================================
The``ansys.eigen.python`` package contains the necessary objects for testing the API REST
and gRPC communication protocols, which are implemented in Python. It also includes two
additional Python packages:

- REST package: ``ansys.eigen.python.rest``
- gRPC package: ``ansys.eigen.python.grpc``

Each of these packages contains two key modules for performing the demos: ``client``
and ``server``. This section is divided into REST and gRPC package subsections.

----------------------------------------
The API REST Eigen Example Python module
----------------------------------------

Import the API REST Python server and client with:

.. code:: python

   import ansys.eigen.python.rest.server as rest_server
   import ansys.eigen.python.rest.client as rest_client


The API REST Python server is a Flask app that contains a SQLite database (DB). You can easily
deploy this server by running commands in the terminal. If you are located at the root directory
of the repository, you can deploy this version of the server with:

.. code:: bash

   export FLASK_APP="src/ansys/eigen/python/rest/server.py"
   flask run

While the preceding commands deploy the server with default parameters, you can deploy it manually by
calling the ``create_app()`` method to return the Flask app and then run it using the ``app.run()``
method:

.. code:: python

   app = rest_server.create_app()
   app.run("127.0.0.1", 1234)

The Python client contains a class called ``DemoRESTClient`` that provides tools for interacting
directly with the deployed server. For example, to create an API REST client for interacting with
the previously deployed server, you would run:

.. code:: python

   client = rest_client.DemoRESTClient("127.0.0.1", 1234)

The client is then made available to perform operations such as:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   vec_add = client.add(vec_1, vec_2)             # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_sub = client.subtract(vec_1, vec_2)        # >>> numpy.ndarray([-4.0, -2.0,  1.0,  4.0])
   vec_mul = client.multiply(vec_1, vec_2)        # >>> 19 (== dot product of vec_1 and vec_2)

----------------------------------------
The API gRPC Eigen Example Python module
----------------------------------------

Import the API gRPC Python server and client with:

.. code:: python

   import ansys.eigen.python.grpc.server as grpc_server
   import ansys.eigen.python.grpc.client as grpc_client


The API gRPC Python server is a standalone gRPC app with no DB. You can easily deploy this server
by running commands in the terminal. If you are located at the root directory of the repository, you
can deploy this version of the server with:

.. code:: bash

   python src/ansys/eigen/python/grpc/server.py

While the preceding command deploys the server with default parameters, you can deploy it manually by
calling the ``serve()`` method inside the module:

.. code:: python

   grpc_server.serve()

The Python client contains a class called ``DemoGRPCClient`` that provides tools for interacting
directly with the deployed server. For example, to create an API gRPC client for interacting with
the previously deployed server, you would run:

.. code:: python

   cli = grpc_client.DemoGRPCClient(ip="127.0.0.1", port=50051)

The client is then made available to perform operations such as:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   cli.request_greeting("James")                  # >>> Server answering  "Hello, James!"
   vec_add = cli.add_vectors(vec_1, vec_2)        # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_mul = cli.multiply_vectors(vec_1, vec_2)   # >>> 19 (== dot product of vec_1 and vec_2)

==============================================
Understanding the API Eigen Example C++ module
==============================================

The``ansys.eigen.python`` package also includes two C++ projects, which are C++ implementations of the
previously explained Python packages:

- C++ REST projects: ``src/ansys/eigen/cpp/rest``
- C++ gRPC projects: ``src/ansys/eigen/cpp/grpc``

Each of these C++ packages contains two key modules for performing the demos: ``client`` and ``server``.
This section is divided into REST and gRPC project subsections.

---------------------------------------
The API REST Eigen Example C++ projects
---------------------------------------

First you must install the projects as per the instructions in :ref:`getting_started`.

Once projects are installed, run these ``include`` commands:

.. code:: cpp

   #include <apieigen/rest/EigenClient.hpp>
   #include <apieigen/rest/RestServer.hpp>


The API REST C++ server is a CrowCpp app that contains a SQLite DB. You can easily deploy this server by running
commands in the terminal.

If you create a simple ``server.cpp`` file, you can do the following:

.. code:: cpp

   #include <apieigen/rest/RestServer.hpp>

   int main() {
      // Let us instantiate our server
      ansys::rest::server::RestServer server{};

      // Start serving!
      server.serve();
   }

Once the library is installed, you can compile the ``server.cpp`` file:

.. code:: bash

   g++ -o myServer server.cpp -lapi_eigen_example_rest_server

You can then run the executable that results from the compilation:

.. code:: bash
   
   ./myServer

You see these messages as your server is being deployed:

.. code:: bash

   >>> Opened database successfully.
   >>> RestDb object created.
   >>> DB tables created successfully.
   >>> (2022-05-13 08:48:54) [INFO    ] REST Server object instantiated.
   >>> (2022-05-13 08:48:54) [INFO    ] Crow/1.0 server is running at http://0.0.0.0:18080 using 16 threads
   >>> (2022-05-13 08:48:54) [INFO    ] Call `app.loglevel(crow::LogLevel::Warning)` to hide Info level logs.

While the preceding command deploys the server with default parameters, you can deploy it with your own custom
parameters by providing optional inputs in the ``serve()`` method.

The C++ client contains a class called ``EigenClient`` that provides tools for interacting
directly with the deployed server. For example, to create an API REST client for interacting with
the previously deployed server, you could write the following code snippet in a new C++ file (for example, ``client.cpp``)
and then call it:

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


The client then deals with a vector addition operation via REST API interaction
with the server, apart from requesting a greeting.

You compile the client with:

.. code:: bash

   g++ -o myClientApp client.cpp -lapi_eigen_example_rest_client

You then run the executable that results from the compilation:

.. code:: bash
   
   ./myClientApp

Enjoy creating your own apps.

---------------------------------------
The API gRPC Eigen Example C++ projects
---------------------------------------

First you must install the projects as per the instructions in :ref:`getting_started`.

Once projects are installed, run these ``include`` commands:

.. code:: cpp

   #include <apieigen/grpc/GRPCClient.hpp>
   #include <apieigen/grpc/GRPCServer.hpp>


The API gRPC C++ server is a standalone gRPC app. You can easily deploy this server by running
commands in the terminal. 

If you create a simple ``server.cpp`` file, you can do the following:

.. code:: cpp

   #include <apieigen/grpc/GRPCServer.hpp>

   int main() {
      // Let us instantiate our server
      ansys::grpc::server::GRPCServer server{};

      // Start serving!
      server.serve();
   }

Once the library is installed, you can compile the ``server.cpp`` file:

.. code:: bash

   g++ -o myServer server.cpp -lapi_eigen_example_grpc_server

You then run the executable that results from the compilation:

.. code:: bash
   
   ./myServer

You see these messages as your server is being deployed:

.. code:: bash

   >>> Instantiating our server...
   >>> GRPCService object created.
   >>> Server listening on 0.0.0.0:50000

While the preceding command deploys the server with default parameters, you can deploy it with your own custom
parameters by providing optional inputs in the ``serve()`` method.

The C++ client contains a class called ``GRPCClient`` that provides tools for interacting
directly with the server. For example, if you wanted to create an API gRPC client for interacting with
the previously deployed server, you would write the following code snippet in a new C++ file (for example, ``client.cpp``)
and then call it:

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


The client then deals with a vector addition operation via gRPC API interaction
with the server, apart from requesting a greeting.

You compile the client app with:

.. code:: bash

   g++ -o myClientApp client.cpp -lapi_eigen_example_grpc_client

You then run the executable that results from the recompilation:

.. code:: bash
   
   ./myClientApp


You see these messages as your server is being deployed:

.. code:: bash

   GRPCClient object created.
   >>>> Requesting greeting for Michael
   >>>> Server answered --> Hello, Michael!
   >>>> Requesting vector addition!
   >>>> Server vector addition successful! Retrieving vector.
   GRPCClient object destroyed.

On the server side, you see these logs:

.. code:: bash

   >>>> Greeting requested! Requested by Michael
   >>>> Vector addition requested!
   >>>> Incoming Vector:  1  2  3 50
   >>>> Incoming Vector:  4  5  8 10
   >>>> Result of addition:  5  7 11 60
   Enjoy creating your own apps!

Enjoy creating your own apps.