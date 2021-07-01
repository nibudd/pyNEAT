import numpy as np
from EdgeGene import EdgeGene
from NodeGene import NodeGene
from NodeType import NodeType
from Genotype import Genotype
from NeuralNetwork import NeuralNetwork
from GenotypeRealizer import realize_neural_network

def test_realizeNeuralNetwork_1input_1output():
    node_0 = NodeGene(NodeType.INPUT, 0)
    node_1 = NodeGene(NodeType.OUTPUT, 1)
    node_genes = [node_0, node_1]

    edge_genes = [EdgeGene(node_0, node_1, 1.1, True, 1)]

    genotype = Genotype(edge_genes, node_genes)

    neural_network = realize_neural_network(genotype)
    expected = NeuralNetwork(np.array([[0, 0], [1.1, 0]]), len(edge_genes))

    assert np.array_equal(expected.weights, neural_network.weights)
    assert expected.max_iterations == neural_network.max_iterations
    

def test_realizeNeuralNetwork_2input_1output():
    node_0 = NodeGene(NodeType.INPUT, 0)
    node_1 = NodeGene(NodeType.INPUT, 1)
    node_2 = NodeGene(NodeType.OUTPUT, 2)
    node_genes = [node_0, node_1, node_2]

    edge_genes = [
        EdgeGene(node_0, node_2, 1, True, 0),
        EdgeGene(node_1, node_2, 2, True, 0)
    ]

    genotype = Genotype(edge_genes, node_genes)

    neural_network = realize_neural_network(genotype)
    expected = NeuralNetwork(np.array([[0, 0, 0], [0, 0, 0], [1, 2, 0]]), len(edge_genes))

    assert np.array_equal(expected.weights, neural_network.weights)
    assert expected.max_iterations == neural_network.max_iterations

def test_realizeNeuralNetwork_2input_1hidden_1output():
    input_1 = NodeGene(NodeType.INPUT, 0)
    input_2 = NodeGene(NodeType.INPUT, 1)
    output_1 = NodeGene(NodeType.OUTPUT, 2)
    hidden_1 = NodeGene(NodeType.HIDDEN, 3)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, True, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0)
    ]

    genotype = Genotype(edge_genes, node_genes)

    neural_network = realize_neural_network(genotype)
    expected = NeuralNetwork(
        np.array([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [1, 2, 0, 4],
                 [3, 0, 0, 0]]),
        len(edge_genes)
    )

    assert np.array_equal(expected.weights, neural_network.weights)
    assert expected.max_iterations == neural_network.max_iterations

def test_realizeNeuralNetwork_2input_1hidden_1output_1loop():
    input_1 = NodeGene(NodeType.INPUT, 0)
    input_2 = NodeGene(NodeType.INPUT, 1)
    output_1 = NodeGene(NodeType.OUTPUT, 2)
    hidden_1 = NodeGene(NodeType.HIDDEN, 3)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, True, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0),
        EdgeGene(hidden_1, hidden_1, 5, True, 0)
    ]

    genotype = Genotype(edge_genes, node_genes)

    neural_network = realize_neural_network(genotype)
    expected = NeuralNetwork(
        np.array([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [1, 2, 0, 4],
                 [3, 0, 0, 5]]),
        len(edge_genes)
    )

    assert np.array_equal(expected.weights, neural_network.weights)
    assert expected.max_iterations == neural_network.max_iterations

def test_realizeNeuralNetwork_2input_1hidden_1output_1loop_1disabled():
    input_1 = NodeGene(NodeType.INPUT, 0)
    input_2 = NodeGene(NodeType.INPUT, 1)
    output_1 = NodeGene(NodeType.OUTPUT, 2)
    hidden_1 = NodeGene(NodeType.HIDDEN, 3)
    node_genes = [input_1, input_2, output_1, hidden_1]

    edge_genes = [
        EdgeGene(input_1, output_1, 1, False, 0),
        EdgeGene(input_2, output_1, 2, True, 0),
        EdgeGene(input_1, hidden_1, 3, True, 0),
        EdgeGene(hidden_1, output_1, 4, True, 0),
        EdgeGene(hidden_1, hidden_1, 5, True, 0)
    ]

    genotype = Genotype(edge_genes, node_genes)

    neural_network = realize_neural_network(genotype)
    expected = NeuralNetwork(
        np.array([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 2, 0, 4],
                 [3, 0, 0, 5]]),
        len(edge_genes)
    )

    assert np.array_equal(expected.weights, neural_network.weights)
    assert expected.max_iterations == neural_network.max_iterations

