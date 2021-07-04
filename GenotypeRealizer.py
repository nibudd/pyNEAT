import numpy as np
from NodeGene import NodeGene
from EdgeGene import EdgeGene
from Genotype import Genotype
from NeuralNetwork import NeuralNetwork


def realize_neural_network(genotype: Genotype) -> NeuralNetwork:
    weights = _get_weights_matrix(genotype)
    outputs = _get_outputs_list(genotype.node_genes)

    return NeuralNetwork(weights, outputs)


def _get_weights_matrix(genotype: Genotype) -> np.array:
    n = _get_number_of_nodes(genotype.node_genes)
    weights = np.zeros((n, n))

    weights = _add_edge_weights(genotype.edge_genes, weights)
    weights = _add_input_memory(genotype.node_genes, weights)


    return weights


def _get_number_of_nodes(node_genes: list[NodeGene]) -> int:
    id_offset_correction = 1 # since node numbers start at 0
    nodes = node_genes[-1].id
    return nodes + id_offset_correction


def _add_edge_weights(edge_genes: EdgeGene, weights: np.array) -> np.array:
    for edge_gene in edge_genes:
        if not edge_gene.enabled:
            continue

        col = edge_gene.in_node.id
        row = edge_gene.out_node.id
        weight = edge_gene.weight

        weights[row, col] = weight

    return weights

def _add_input_memory(node_genes: list[NodeGene], weights: np.array) -> np.array:
    input_gene_ids = [node_gene.id for node_gene in node_genes if node_gene.is_input()]
    for input_gene_id in input_gene_ids:
        weights[input_gene_id, input_gene_id] = 100

    return weights

def _get_outputs_list(node_genes: list[NodeGene]) -> list[int]:
    return [node_gene.id for node_gene in node_genes if node_gene.is_output()]