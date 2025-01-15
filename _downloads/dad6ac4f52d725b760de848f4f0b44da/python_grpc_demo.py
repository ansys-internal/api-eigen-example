"""
.. _ref_grpc_demo_python:

API Eigen Example - gRPC Demo using Python
------------------------------------------

This tutorial shows how you can use the Python gRPC Client of the API Eigen Example
project to communicate with the gRPC Server.

In the following demo, we will be showing the basics of API gRPC protocol by means of a
simple library we have created. This library basically contains two elements in its Python version:

- A server which basically implements an API gRPC interface to communicate with an installed library within
    it, in our case the Eigen library. This API gRPC interface basically exposes certain functionalities such as
    adding, subtracting and multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` in a simple way. By using Protobuf,
    we have created certain messages which both the server and the client know how to encode and decode.
- A client in charge of easing the interaction with the server by means of API gRPC interface specific methods.

In order to run this demo, it is necessary to deploy a server. When the docs are generated
(via workflows), the server is deployed as a service to compile the example. However, if you
are planning on running the example on your own, it is necessary to deploy it manually. In order to
do so, please run this on a different Python terminal:

>>> import ansys.eigen.python.grpc.server as grpc_server
>>> import logging
>>> logging.basicConfig()
>>> grpc_server.serve()

Now, once the server is up and running. Let us import our client!

"""

from ansys.eigen.python.grpc.client import DemoGRPCClient

###############################################################################
# The DemoGRPCClient
# ~~~~~~~~~~~~~~~~~~
# This ``DemoGRPCClient`` class is basically the one which will handle the API gRPC interface with the server,
# together with the connection itself, the formatting of the request and so on. When constructing the class we
# must provide as inputs the ``ip`` and the ``port`` of the server. For this demo we are running, since we
# already deployed the server (either manually or as a container), we will provide the following arguments:
#
# - IP(or DNS): 127.0.0.1
# - Port: 50051
#
# The server is exposed by **IP 127.0.0.1** and **port 50051** as per defined in the Dockerfile of the server and
# the server itself. Thus, the previous inputs should be provided, although they are also the default values. Nonetheless,
# in the IP field we could also provide the DNS for the sake of showing that DNS values are also accepted. In this case,
# by inserting ``localhost`` the connection would also be established.

print("=========================")
my_client = DemoGRPCClient(ip="127.0.0.1", port=50051)
print("=========================")
my_client_dns = DemoGRPCClient(ip="localhost", port=50051)


###############################################################################
# This ``DemoGRPCClient`` also has a method for verifying the connection to out client, which is a simple
# handshake/greeting, when we provide our name:

print("=========================")
my_client.request_greeting("User")

###############################################################################
# This will let us verify that the connection to the server is adequate and communication is favorable.

# Now, we will proceed to perform a simple operation like adding two 1D numpy.ndarrays. First, let us start by defining them:

import numpy as np

vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

###############################################################################
# Performing gRPC interaction
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Now, we will call the client method ``add_vectors(...)``, and we will explain the typical process of all interface methods (``add_XXXX(...)`` and ``multiply_XXXX(...)``):
#
# - The client performs some sanity checks to confirm that the inputs provided are as expected. This Demo has some limitations such as: only 1D, 2D numpy.ndarrays are allowed; they must be of type float64. Direct interaction with the server (i.e. without a client) and using gRPC is out of the scope of this demo. Doing so could be considered as "impossible" since you would have to serialize your message on your own, following the standard defined in the proto files.
#
# - The client serializes the messages with the inputs provided using generator functions. Our end server is characterized for receiving ``streams`` of messages, which basically represent a list of messages. Each of these messages are serialized following the interface proposed by the proto files, thanks to the automatically generated source code by protobuf.
#     - For example our ``Vector`` message is characterized for having the following structure:
#
#           ``enum DataType {INTEGER = 0;DOUBLE = 1;}``
#
#           ``message Vector {DataType data_type = 1; int32 vector_size = 2; bytes vector_as_chunk = 3;}``
#
# - When the server receives the messages, it deserializes them and interprets each of the previous fields. Thus, it is easily converted into a numpy.ndarray of the adequate type. Then, the desired vectors to be added are passed to the Eigen library via our ``demo_eigen_wrapper`` for the resolution of the demanded operation.
#
# - Once the results of the operation are available, the server serializes the result and responds with the adequate message to the client.
#     - For example, according to the proto file, our server receives a stream of Vector messages, and returns a single Vector message (which contains the result of the requested operation):
#
#           ``rpc AddVectors(stream Vector) returns (Vector) {}``
#
# - The client then receives the response, deserializes the message and returns the corresponding result to the end-user as numpy.ndarray. Thus, the entire process is like a black-box for the end-user, and does not require to understand what is happening behind the scenes, since the end-user is only interested in the end-result.
#
# Let us now call the method!

# Call the client to perform your desired operation
vec_add = my_client.add_vectors(vec_1, vec_2)

# Show the result!
print("Vector addition!")
print("================")
print(vec_add)

###############################################################################
# As mentioned before, there are several other methods implemented:

# Call the client to perform your desired operation
vec_flip = my_client.flip_vector(vec_1)

# Show the result!
print("Vector position-flip!")
print("====================")
print(vec_flip)

###############################################################################

# Call the client to perform your desired operation
vec_mul = my_client.multiply_vectors(vec_1, vec_2)

# Show the result!
print("Vector dot product!")
print("===================")
print(vec_mul)

###############################################################################
# Let us show as well operations with 2D numpy.ndarrays (i.e. Matrices)

# Define your matrices
mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

# Call the client to perform your desired operation
mat_add = my_client.add_matrices(mat_1, mat_2)

# Show the result!
print("Adding matrices!")
print("================")
print(mat_add)

###############################################################################

# Call the client to perform your desired operation
mat_mul = my_client.multiply_matrices(mat_1, mat_2)

# Show the result!
print("Multiplying matrices!")
print("=====================")
print(mat_mul)
