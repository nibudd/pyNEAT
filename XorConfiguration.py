import numpy as np
from Genotype import Genotype
from NodeGene import NodeGene
from NodeType import NodeType
from PhenotypeUtility import construct_weights_matrix, construct_input_vector, extract_output_vector
from NeuralNetworkRunner import run_neural_network
from StandardConfig import *

def get_starting_node_genes() -> list[NodeGene]:
    return [
        NodeGene(NodeType.BIAS, 0),
        NodeGene(NodeType.INPUT, 1),
        NodeGene(NodeType.INPUT, 2),
        NodeGene(NodeType.OUTPUT, 3)
    ]

def evaluate_fitness(genotype: Genotype) -> float:
    W = construct_weights_matrix(genotype)
    inputs = [
        np.array([[0, 0]]).T,
        np.array([[0, 1]]).T,
        np.array([[1, 0]]).T,
        np.array([[1, 1]]).T
    ]
    expected_outputs = [
        np.array([[0]]),
        np.array([[1]]),
        np.array([[1]]),
        np.array([[0]])
    ]
    outputs = []

    for input in inputs:
        x = construct_input_vector(genotype.node_genes, input)
        y = run_neural_network(W, x, transfer_function)
        outputs.append(extract_output_vector(genotype.node_genes, y))

    error = 0
    for i in range(len(expected_outputs)):
        error += abs(expected_outputs[0, 0] - outputs[0, 0])

    return (4.0 - error) ** 2
