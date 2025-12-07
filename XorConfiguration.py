import numpy as np

from Genotype import Genotype
from NodeGene import NodeGene, BiasNodeGene, InputNodeGene, OutputNodeGene
from PhenotypeUtility import evaluate_feedforward
from StandardConfig import StandardConfig


class XorConfiguration(StandardConfig):

    @staticmethod
    def get_starting_node_genes() -> list[NodeGene]:
        return [BiasNodeGene(0), InputNodeGene(1), InputNodeGene(2), OutputNodeGene(3)]

    @staticmethod
    def evaluate_fitness(genotype: Genotype) -> float:
        inputs = [
            np.array([0, 0]),
            np.array([0, 1]),
            np.array([1, 0]),
            np.array([1, 1]),
        ]
        expected_outputs = [0, 1, 1, 0]

        error = 0
        for i, inp in enumerate(inputs):
            output = evaluate_feedforward(
                genotype, inp, XorConfiguration.transfer_function
            )
            error += abs(expected_outputs[i] - output[0, 0])

        return (4.0 - error) ** 2
