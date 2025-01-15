.. _docker_examples:

===============
Docker examples
===============
As part of the development of this project, several Docker images were created to allow
direct use of the client and server modules for both REST and gRPC using Python and C++.
You can refer to demo section of interest to you.
 
*********************
REST API using Python
*********************

For this demo, the following Docker containers are available:

- ``python-rest-client``: Docker container with the needed packages for running the implemented client (from ``from ansys.eigen.python.rest.client import DemoRESTClient``)
- ``python-rest-server``: Docker container with the needed packages for running the server with the Eigen library solver

These Docker containers are available at the GitHub Container Registry. You can download the latest version with:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/python-rest-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/python-rest-client:latest

However, you can also build these Docker containers manually from the root directory of the repository with:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-server -f docker/python-rest-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-client -f docker/python-rest-client/Dockerfile .

The server Docker image is a standalone Flask app that starts whenever the image is run. This way,
you do not have to perform any other operation apart from running the Docker image.

To run the server Docker image manually, you must run:

.. code:: bash

    docker run -d -p 5000:5000 -it ghcr.io/ansys/api-eigen-example/python-rest-server:latest

The client Docker image is a standalone JupyterLab app that starts whenever the image is run. This JupyterLab
app contains a demo Jupyter Notebook that you can run to test the client itself. Furthermore, you can open a new
Jupyter Notebook within JupyterLab and start creating your own app.

To run the client Docker image manually, you must run:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/python-rest-client:latest

However, deploying Docker containers manually is not the easiest way to test them. To start playing around with
them, you can use the docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/python-rest/docker-compose.yml.
This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them
because they are located in the same Docker network.

To launch the Docker compose task, simply run the following wherever the ``docker-compose.yml`` file is located:

.. code:: bash

    docker-compose up -d

You can then start playing around with the Docker compose demo.

*********************
gRPC API using Python
*********************

For this demo, the following Docker containers are available:

- ``python-grpc-client``: Docker container with the needed packages for running the implemented client (from ``ansys.eigen.python.grpc.client import DemoGRPCClient``)
- ``python-grpc-server``: Docker container with the needed packages for running the server with the Eigen library solver

These Docker containers are available at the GitHub Container Registry. You can download the latest version with:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/python-grpc-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/python-grpc-client:latest

However, you can also build these Docker containers manually from the root directory of the repository with:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-server -f docker/python-grpc-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-client -f docker/python-grpc-client/Dockerfile .

The server Docker image is a standalone gRPC server that starts whenever the image is run. This way,
you do not have to perform any other operation apart from running the Docker image.

To run the server Docker image manually, you must run:

.. code:: bash

    docker run -d -p 50051:50051 -it ghcr.io/ansys/api-eigen-example/python-grpc-server:latest

The client Docker image is a standalone JupyterLab app that starts whenever the image is run. This JupyterLab
app contains a demo Jupyter Notebook that you can run to test the client itself. Furthermore, you can open a new
Jupyter Notebook within the JupyterLab and start creating your own app.

To run the client Docker image manually, you must run:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/python-grpc-client:latest

However, deploying Docker containers manually is not the easiest way to test them. To start playing around with
them, you can use the docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/python-grpc/docker-compose.yml.
This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them
because they are located in the same Docker network.

To launch the Docker compose task, simply run the following command wherever the ``docker-compose.yml`` file is located:

.. code:: bash

    docker-compose up -d

You can then start playing around with the Docker compose demo.

******************
REST API using C++
******************

For this demo, the following Docker containers are available:

- ``cpp-rest-client``: Docker container with the needed packages for running the implemented client (``#include <apieigen/rest/EigenClient.hpp>``)
- ``cpp-rest-server``: Docker container with the needed packages for running the server with the Eigen library solver

These Docker containers are available at the GitHub Container Registry. You can download the latest version with:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest

However, you can also build these Docker containers manually from the root directory of the repository with:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-server -f docker/cpp-rest-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-client -f docker/cpp-rest-client/Dockerfile .

The server Docker image is a standalone `CrowCpp <https://crowcpp.org/>`_ app that starts whenever the image is run. This way,
you do not have to perform any other operation apart from running the Docker image.

To run the server Docker image manually, you must run:

.. code:: bash

    docker run -d -p 18080:18080 -it ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest

The client Docker image is a standalone JupyterLab app that starts whenever the image is run. This JupyterLab
app contains a demo Jupyter Notebook that you can run to test the client itself. Furthermore, you can open a new
Jupyter Notebook within JupyterLab and start creating your own app.

To run the client Docker image manually, you must run:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest

Even though dealing with a C++ implementation, thanks to `cling <https://root.cern/cling/>`_ and
`xeus-cling <https://github.com/jupyter-xeus/xeus-cling>`_, this demo is capable of demonstrating
via Jupyter Notebooks the functionalities of the C++ client as if it were an interpretable language (like Python or Matlab). 
Special thanks to their contributors for these great packages.

However, deploying Docker containers manually is not the easiest way to test them. To start playing around with
them, you can use the docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/cpp-rest/docker-compose.yml.
This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them
because they are be located in the same Docker network.

To launch the Docker compose task, simply run the following command where the ``docker-compose.yml`` file is located:

.. code:: bash

    docker-compose up -d

You can then start playing around with the Docker compose demo.

******************
gRPC API using C++
******************

For this demo, the following Docker containers are available:

- ``cpp-grpc-client``: Docker container with the needed packages for running the implemented client (``#include <apieigen/grpc/GRPCClient.hpp>``)
- ``cpp-grpc-server``: Docker container with the needed packages for running the server with the Eigen library solver

These Docker containers are available at the GitHub Container Registry. You can download the latest version with:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/cpp-grpc-client:latest

However, you can also build these Docker containers manually from the root directory of the repository with:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-grpc-server -f docker/cpp-grpc-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-grpc-client -f docker/cpp-grpc-client/Dockerfile .

The server Docker image is a standalone gRPC app that starts whenever the image is run. This way,
you do not have to perform any other operation apart from running the Docker image.

To run the server Docker image manually, you must run:

.. code:: bash

    docker run -d -p 50000:50000 -it ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest

The client Docker image is a standalone JupyterLab app that starts whenever the image is run. This JupyterLab
app contains a demo Jupyter Notebook that you can run to test the client itself. Furthermore, you can open a new Jupyter
Notebook within JupyterLab and start creating your own app.

To run the client Docker image manually, you must run:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/cpp-grpc-client:latest

Even though dealing with a C++ implementation, thanks to `cling <https://root.cern/cling/>`_ and
`xeus-cling <https://github.com/jupyter-xeus/xeus-cling>`_, this demo is capable of demonstrating
via Jupyter Notebooks the functionalities of the C++ client as if it were an interpretable language (like Python or Matlab). 
Special thanks to their contributors for these great packages.

However, deploying the Docker containers manually is not the easiest way to test them. To start playing around with
them, you can use the docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/cpp-grpc/docker-compose.yml.
This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them
because they are located in the same Docker network.

To launch the Docker compose task, simply run the following command wherever the ``docker-compose.yml`` file is located:

.. code:: bash

    docker-compose up -d

You can then start playing around with the Docker compose demo.