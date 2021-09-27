import numpy as np

import NodeGeneFactory
from PhenotypeUtility import construct_input_vector


def test_constructs_input_vector():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    inputs_only = np.array([[1, 2]]).T
    inputs = construct_input_vector(node_genes, inputs_only)
    expected = np.array([[1, 2, 0, 0]]).T

    assert np.array_equal(expected, inputs)


def test_constructs_input_vector_with_bias():
    bias = NodeGeneFactory.make_bias(0)
    input_1 = NodeGeneFactory.make_input(1)
    input_2 = NodeGeneFactory.make_input(2)
    output_1 = NodeGeneFactory.make_output(3)
    hidden_1 = NodeGeneFactory.make_hidden(4, 0)
    node_genes = [bias, input_1, input_2, output_1, hidden_1]

    inputs_only = np.array([[.1, .2]]).T
    inputs = construct_input_vector(node_genes, inputs_only)
    expected = np.array([[1, .1, .2, 0, 0]]).T

    assert np.array_equal(expected, inputs)
