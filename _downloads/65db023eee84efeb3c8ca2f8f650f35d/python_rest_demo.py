"""
.. _ref_rest_demo_python:

API Eigen Example - REST Demo using Python
------------------------------------------

This demo shows how you can use the Python REST client of the API Eigen Example
project to communicate with the REST server. It uses a simple Python library to
show the basics of API REST protocols. This library contains two elements:

- A server that implements an API REST interface to communicate with an installed library within
    it, which is the Eigen library. This API REST interface exposes functionalities such as
    adding, subtracting and multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` in a simple way.
- A client in charge of easing the interaction with the server by means of API REST-specific methods.
    When using the client library, you do not need to know the specifics of the API REST interface.

To run this demo, you must deploy a server. When the docs are generated
(via workflows), the server is deployed as a service to compile the example. However, if you
are planning on running the example on your own, you must deploy it manually by running these commands
on a different Python terminal:

>>> import ansys.eigen.python.rest.server as rest_server
>>> app = rest_server.create_app()
>>> app.run("127.0.0.1", 5000)

Once the server is up and running, you can import your client:

"""

from ansys.eigen.python.rest.client import DemoRESTClient

###############################################################################
# The DemoRESTClient
# ~~~~~~~~~~~~~~~~~~
# The ``DemoRESTClient`` class handles the API REST interface with the server,
# together with the connection itself, the formatting of the request, and more. When
# constructing the class, you must provide as inputs the ``host`` and ``port`` of the server. For this
# demo, since the server is already deployed (either manually or as a service in a container),
# use the following arguments:
#
# - Host: http://127.0.0.1
# - Port: 5000
#
# The server is exposed by **IP 127.0.0.1** and **port 5000** as per defined in the Dockerfile of the server
# (or if deployed manually, as specified previously). Thus, the previous inputs should be provided.
#
# The ``DemoRESTClient`` class also allows for basic authentication in case the server was to be protected.
# See below how to provide the ``user`` and ``pwd`` in this example:

my_client = DemoRESTClient("http://127.0.0.1", 5000)
my_client_ba = DemoRESTClient("http://127.0.0.1", 5000, user="myUser", pwd="myPwd")

###############################################################################
# The ``DemoRESTClient`` also has a method for retrieving the connection details of the client:

print("=========================")
my_client.get_connection_details()
print("=========================")
my_client_ba.get_connection_details()

###############################################################################
# Now, perform a simple operation like adding two 1D numpy.ndarrays. Start by defining them:

import numpy as np

vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

###############################################################################
# Performing REST interaction
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Explanations follow for the typical process of all interface methods (``add()``, ``subtract()`` and ``multiply()``):
#
# - The client performs some sanity checks to confirm that the inputs provided are as expected. This demo has some limitations, such as only allowing 1D and 2D numpy.ndarrays of the float64 type. However, to interact directly with the server, you must take other considerations into account regarding the format of your requests, which is why a client library is used).
# - Once the client has checked that everything is fine, it posts available resources. Here is where the REST world starts:
#     - Servers expose resources, also known as entities, which are well understood if we compare them to objects. For example, if we want to POST a RESOURCE we should basically:
#         - ``POST`` to ``${server-uri}/${resource}`` --> In the demo: ``http://127.0.0.1:5000/Vectors``
#         - The Demo server has two resources implemented: ``Matrices`` and ``Vectors``. Hence, it can handle only 1D and 2D numpy.ndarrays.
#     - When POSTing a resource, the request body contains the resource's information. For example, the request contains the 1D numpy.ndarray that you want to POST). This information is usually serialized into a JSON format. The expected keys must be known by the client and the server to allow a proper interfacing. In a real REST application, the server usually exposes its metadata, which is basically the schema or structure of the different entities implemented (such as their names and attributes). This way, you know how to interact with the server without knowing the specifics of the implementation.
#         - Imagine if you were to use CURL commands. The POST request for your first vector would look something like this:
#         - ``curl -X POST "http://127.0.0.1:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[5, 23, 3, 4]}'``
#     - If the POST was successful, you would receive an HTTP response that contains in its body the ID of the posted resource:
#         - ``{"vector" : {"id" : 1235412 }}``
#     - The server contains a database (DB) in which the resources posted are stored and retrieved from.
# - After POSTings are performed, you proceed to ask the server for a certain operation involving the resources submitted.
#     - Servers can also admit operations. A typical standard for defining operation endpoints would be:
#         - ``GET`` to ``${server-uri}/${operation}/${resource}`` --> In the demo: ``http://127.0.0.1:5000/add/Vectors``
#     - These GET requests also contain in their bodies the IDs of the involved resources:
#         - Imagine if you were to use CURL commands. The GET request for adding two vectors would look something like this:
#         - ``curl -X GET "http://127.0.0.1:5000/add/Vectors" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'``
#     - The server then interacts with the DB, retrieves the vectors, calls the Eigen library (via a dedicated wrapper using pybind11), performs the operation, and returns the result.
#     - The client then receives a response containing the result of the operation:
#         - ``{"vector-addition" : {"result" : [2.0, 3.0, 5.0, 4.0] }}``
#         - The dedicated client implemented then parses this JSON string and transforms the resulting value into a numpy.ndarray.
#         - This way, you call the client library with numpy.ndarrays and retrieve numpy.ndarrays without having to know the specifics of the interface.
#
#

# Call the client to perform your desired operation
# For example, call the client method ``add()``:
vec_add = my_client.add(vec_1, vec_2)

# Show the result
print("Vector addition!")
print("================")
print(vec_add)

###############################################################################
# As mentioned before, there are several other methods implemented:

# Call the client to perform your desired operation
vec_sub = my_client.subtract(vec_1, vec_2)

# Show the result!
print("Vector subtraction!")
print("===================")
print(vec_sub)

###############################################################################

# Call the client to perform your desired operation
vec_mul = my_client.multiply(vec_1, vec_2)

# Show the result!
print("Vector dot product!")
print("===================")
print(vec_mul)

###############################################################################
# Here are some operations with 2D numpy.ndarrays (matrices)

# Define your matrices
mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

# Call the client to perform your desired operation
mat_add = my_client.add(mat_1, mat_2)

# Show the result
print("Adding matrices.")
print("================")
print(mat_add)

###############################################################################

# Call the client to perform your desired operation
mat_sub = my_client.subtract(mat_1, mat_2)

# Show the result!
print("Subtracting matrices.")
print("=====================")
print(mat_sub)

###############################################################################

# Call the client to perform your desired operation
mat_mul = my_client.multiply(mat_1, mat_2)

# Show the result!
print("Multiplying matrices.")
print("=====================")
print(mat_mul)
