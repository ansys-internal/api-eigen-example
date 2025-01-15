.. _bm_results:

=================
Benchmark results
=================

One of the tasks of this project is to evaluate the performance of different implementations, including using REST versus gRPC
and the impact of the language used. This page displays the latest benchmark test results uploaded to the repository.

Subsequent sections categorize these test results according to their implementation language. All sections have the this set of
tests for both protocols:

* Adding two vectors of multiple sizes
* Performing a dot product of two vectors of multiple sizes
* Adding two square matrices of multiple sizes
* Multiplying two matrices of multiple sizes

Graphs show the parametrized sizes for these benchmark tests. The graphs are basically a sequence of powers of 2 (that is,
2, 4, 8, 16, and so on). The final value is currently set to 2048, but it is easily adaptable.

**********************
Benchmark test results
**********************

Layout
~~~~~~

The layout of all figures show results for benchmark tests parametrized as:
  * Language implementation: Python, C++
  * API Protocol: REST, gRPC
  * Number of elements in data structures (that is, size of vector, matrix)

Adding vectors
~~~~~~~~~~~~~~

.. raw:: html
    :file: images/add_vectors.svg

Multiplying vectors
~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/multiply_vectors.svg

Adding matrices
~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/add_matrices.svg

Multiplying matrices
~~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/multiply_matrices.svg

