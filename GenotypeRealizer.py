import numpy as np
from Genotype import Genotype
from NeuralNetwork import NeuralNetwork


def realize_neural_network(genotype: Genotype) -> NeuralNetwork:
    weights = _get_weights_matrix(genotype)
    max_iterations = len(genotype.edge_genes)

    return NeuralNetwork(weights, max_iterations)


def _get_weights_matrix(genotype: Genotype) -> np.array:
    n = genotype.node_genes[-1].id + 1
    weights = np.zeros((n, n))

    for edge_gene in genotype.edge_genes:
        if not edge_gene.enabled:
            continue

        col = edge_gene.in_node.id
        row = edge_gene.out_node.id
        weight = edge_gene.weight

        weights[row, col] = weight

    return weights
