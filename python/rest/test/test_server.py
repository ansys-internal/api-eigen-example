import json

import numpy as np
import pytest

from python.rest.server import create_app


@pytest.fixture(scope="module")
def testing_client():
    # Create the app
    app = create_app()
    app.testing = True

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


def test_server_ops_vectors(testing_client):
    """Unit test to verify that the server returns the expected response
    when performing the addition and multiplication of two numpy arrays (as vectors)."""

    # Define your vectors
    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    # Post them to the test server
    response_1 = testing_client.post("/Vectors", json={"value": vec_1.tolist()})
    response_2 = testing_client.post("/Vectors", json={"value": vec_2.tolist()})

    # Check that the posting has been done correctly, and retrieve the IDs
    assert response_1.status_code == 201
    id_1 = json.loads(response_1.text)["vector"]["id"]
    assert response_2.status_code == 201
    id_2 = json.loads(response_2.text)["vector"]["id"]

    # Perform the addition operation and check its status
    response_add = testing_client.get("/add/Vectors", json={"id1": id_1, "id2": id_2})
    assert response_add.status_code == 200
    value = json.loads(json.loads(response_add.text)["vector-addition"]["result"])

    # Check the values of the operation's response
    assert value[0] == 6
    assert value[1] == 6
    assert value[2] == 5
    assert value[3] == 4

    # Perform the multiplication operation and check its status
    response_mul = testing_client.get(
        "/multiply/Vectors", json={"id1": id_1, "id2": id_2}
    )
    assert response_mul.status_code == 200
    value = json.loads(json.loads(response_mul.text)["vector-multiplication"]["result"])

    # Check the values of the operation's response
    assert value == 19


def test_server_ops_matrices(testing_client):
    """Unit test to verify that the server returns the expected response
    when performing the addition and multiplication of two numpy arrays (as matrices)."""

    # Define your matrices
    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    # Post them to the test server
    response_1 = testing_client.post("/Matrices", json={"value": mat_1.tolist()})
    response_2 = testing_client.post("/Matrices", json={"value": mat_2.tolist()})

    # Check that the posting has been done correctly, and retrieve the IDs
    assert response_1.status_code == 201
    id_1 = json.loads(response_1.text)["matrix"]["id"]
    assert response_2.status_code == 201
    id_2 = json.loads(response_2.text)["matrix"]["id"]

    # Perform the addition operation and check its status
    response_add = testing_client.get("/add/Matrices", json={"id1": id_1, "id2": id_2})
    assert response_add.status_code == 200
    value = json.loads(json.loads(response_add.text)["matrix-addition"]["result"])

    # Check the values of the operation's response
    assert value[0][0] == 6
    assert value[0][1] == 6
    assert value[1][0] == 5
    assert value[1][1] == 4

    # Perform the multiplication operation and check its status
    response_mul = testing_client.get(
        "/multiply/Matrices", json={"id1": id_1, "id2": id_2}
    )
    assert response_mul.status_code == 200
    value = json.loads(json.loads(response_mul.text)["matrix-multiplication"]["result"])

    # Check the values of the operation's response
    assert value[0][0] == 9
    assert value[0][1] == 4
    assert value[1][0] == 23
    assert value[1][1] == 12


def test_server_main_error_cases(testing_client):
    """Testing of main error-case scenarios when directly interacting with the server."""
    # Test 1: check that the POST request contains a JSON body
    with pytest.raises(RuntimeError) as e_info:
        testing_client.post("/Matrices")
        assert (
            str(e_info.value)
            == "No JSON-format (i.e. application/json) body was provided in the request."
        )

    # Test 2: check that the POST request contains a JSON body with the expected parameter "value"
    with pytest.raises(RuntimeError) as e_info:
        testing_client.post("/Matrices", json={"mycar": 2})
        assert (
            str(e_info.value) == "No matrix has been provided. Expected key: 'value'."
        )

    # Test 3: check that the POST request contains a JSON body with the expected parameter "value"
    # and that the value itself is a numpy.ndarray
    with pytest.raises(RuntimeError) as e_info:
        testing_client.post("/Matrices", json={"value": "a string"})
        assert (
            str(e_info.value)
            == "Error encountered when transforming input string into numpy.ndarray."
        )

    # We will know perform some actual posts to test the operation error cases
    #
    # Values extracted from test_server_ops_matrices()
    #
    # Define your matrices
    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    # Post them to the test server
    response_1 = testing_client.post("/Matrices", json={"value": mat_1.tolist()})
    response_2 = testing_client.post("/Matrices", json={"value": mat_2.tolist()})

    # Check that the posting has been done correctly, and retrieve the IDs
    assert response_1.status_code == 201
    id_1 = json.loads(response_1.text)["matrix"]["id"]
    assert response_2.status_code == 201
    id_2 = json.loads(response_2.text)["matrix"]["id"]

    # Test 4: check that the GET request contains a JSON body
    with pytest.raises(RuntimeError) as e_info:
        testing_client.get("/add/Matrices")
        assert (
            str(e_info.value)
            == "No JSON-format (i.e. application/json) body was provided in the request."
        )

    # Test 5: check that the GET request contains a JSON body with the expected fields
    with pytest.raises(RuntimeError) as e_info:
        testing_client.get("/add/Matrices", json={"id1": id_1, "value": "a string"})
        assert (
            str(e_info.value)
            == "Arguments for addition operation with matrix are not provided. Expected keys: 'id1', 'id2'."
        )

    # Test 6: in case the given ID does not exist...
    with pytest.raises(RuntimeError) as e_info:
        testing_client.get("/add/Matrices", json={"id1": 0, "id2": id_2})
        assert (
            str(e_info.value)
            == "Unexpected error... No values in the DB for id 0 and type Matrix."
        )
        testing_client.get("/add/Matrices", json={"id1": id_1, "id2": 0})
        assert (
            str(e_info.value)
            == "Unexpected error... No values in the DB for id 0 and type Matrix."
        )