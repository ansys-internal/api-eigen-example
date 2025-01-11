API Eigen Example Documentation |version|
=========================================

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   users_guide/index
   api/index
   docker/index
   examples/index
   benchmark/index
   contributing

Introduction
------------
The API Eigen Example package is a simple demo project for showing PyAnsys users and developers the
differences between the API REST communication protocol and the gRPC communication protocol, which is
used extensively in PyAnsys libraries.

The main goal of this demo project is to expose the `Eigen library <https://eigen.tuxfamily.org/index.php?title=Main_Page>`_
to end users via a client-server interaction that can be implemented using API REST or gRPC communication protocols.

The server exposes certain functionalities of the Eigen library, such as adding and
multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` objects. The computational operations are
performed in the Eigen Library installed within the server, and the results are returned to the
end user (or client). Thus, it is not necessary for the client to have the Eigen library installed.

The client is intended to aid end users because it provides them with tools for communicating with the server
without needing to know the specifics of the protocol implemented. However, you can use CURL commands to interact
directly with the server via API REST communication.

This demo project contains four different examples:

- A **Python REST API** demo using both client-server features, which has
  a wrapping over the Eigen library using pybind11.
- A **Python gRPC API** demo using both client-server features, which
  has a wrapping over the Eigen library using pybind11.
- A **C++ REST API** demo using both client-server features, 
  with direct interaction with the Eigen Library on the server side.
- A **C++ gRPC API** demo using both client-server features, with
  direct interaction with the Eigen Library on the server side.

Features
--------
This demo package provides these primary features:

- A client providing end users with the ability to perform server-side operations
  without knowing details on the communication protocol being employed
- Core examples on how to expose a service (that is, the Eigen Library) via a server using
  different communication protocols.
- Benchmark tests showing the performance of each of the client-server and programming
  language implementations.

Project index
-------------

* :ref:`genindex`
