import numpy as np

from EdgeGene import EdgeGene
import NodeGeneFactory
from Genotype import Genotype
from PhenotypeUtility import construct_weights_matrix, construct_input_vector, extract_output_vector

def test_constructWeightsMatrix_1input_1output():
    node_0 = NodeGeneFactory.make_input(0)
    node_1 = NodeGeneFactory.make_output(1)
    node_genes = [node_0, node_1]

    edge_genes = [EdgeGene(node_0, node_1, 1.1, True, 1)]

    genotype = Genotype(node_genes, edge_genes)

    neural_network = construct_weights_matrix(genotype)
    expected = np.array([[100, 0], [1.1, 0]])

    assert np.array_equal(expected, neural_network)


def test_constructWeightsMatrix_2input_1output():
    node_0 = NodeGeneFactory.make_input(0)
    node_1 = NodeGeneFactory.make_input(1)
    node_2 = NodeGeneFactory.make_output(2)
    node_genes = [node_0, node_1, node_2]

    edge_genes = [
        EdgeGene(node_0, node_2, 1, True, 0),
        EdgeGene(node_1, node_2, 2, True, 0)
    ]

    genotype = Genotype(node_genes, edge_genes)

    neural_network = construct_weights_matrix(genotype)
    expected = np.array([[100, 0, 0], [0, 100, 0], [1, 2, 0]])

    assert np.array_equal(expected, neural_network)

def test_constructWeightsMatrix_2input_1hidden_1output():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, True, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0)
    ]

    genotype = Genotype(node_genes, edge_genes)

    neural_network = construct_weights_matrix(genotype)
    expected = np.array([[100, 0, 0, 0],
                         [0, 100, 0, 0],
                         [1, 2, 0, 4],
                         [3, 0, 0, 0]])

    assert np.array_equal(expected, neural_network)

def test_constructWeightsMatrix_2input_1hidden_1output_1loop():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, True, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0),
        EdgeGene(hidden_1, hidden_1, 5, True, 0)
    ]

    genotype = Genotype(node_genes, edge_genes)

    neural_network = construct_weights_matrix(genotype)
    expected = np.array([[100, 0, 0, 0],
                         [0, 100, 0, 0],
                         [1, 2, 0, 4],
                         [3, 0, 0, 5]])

    assert np.array_equal(expected, neural_network)

def test_constructWeightsMatrix_2input_1hidden_1output_1loop_1disabled():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, False, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0),
        EdgeGene(hidden_1, hidden_1, 5, True, 0)
    ]

    genotype = Genotype(node_genes, edge_genes)

    neural_network = construct_weights_matrix(genotype)
    expected = np.array([[100, 0, 0, 0],
                         [0, 100, 0, 0],
                         [0, 2, 0, 4],
                         [3, 0, 0, 5]])

    assert np.array_equal(expected, neural_network)

def test_constructInputVector():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    inputs_only = np.array([[1,2]]).T
    inputs = construct_input_vector(node_genes, inputs_only)
    expected = np.array([[1,2,0,0]]).T

    assert np.array_equal(expected, inputs)

def test_constructInputVector_with_bias():
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

def test_extractOutputVector():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    nn_outputs = np.array([[1,2, 3, 4]]).T
    outputs = extract_output_vector(node_genes, nn_outputs)
    expected = np.array([[3]]).T

    assert np.array_equal(expected, outputs)
