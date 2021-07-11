import numpy as np
from Genotype import Genotype
import NodeGeneFactory
from NodeGene import NodeGene
from PhenotypeUtility import construct_weights_matrix, construct_input_vector, extract_output_vector
from NeuralNetworkRunner import NeuralNetworkRunner
import StandardConfig


class XorConfiguration(StandardConfig):

    @staticmethod
    def get_starting_node_genes() -> list[NodeGene]:
        return [
            NodeGeneFactory.make_bias(0),
            NodeGeneFactory.make_input(1),
            NodeGeneFactory.make_input(2),
            NodeGeneFactory.make_output(3)
        ]

    @staticmethod
    def evaluate_fitness(genotype: Genotype, nn_runner: NeuralNetworkRunner) -> float:
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
            y = nn_runner.run(W, x)
            outputs.append(extract_output_vector(genotype.node_genes, y))

        error = 0
        for i in range(len(expected_outputs)):
            error += abs(expected_outputs[0, 0] - outputs[0, 0])

        return (4.0 - error) ** 2
