import numpy as np
from NodeGene import NodeGene
from EdgeGene import EdgeGene
from Genotype import Genotype


def construct_weights_matrix(genotype: Genotype) -> np.array:
    n = _get_number_of_nodes(genotype.node_genes)
    weights = np.zeros((n, n))

    weights = _add_edge_weights(genotype.edge_genes, weights)
    weights = _add_input_memory(genotype.node_genes, weights)

    return weights

def construct_input_vector(node_genes: list[NodeGene], input: np.array) -> np.array:
    n = _get_number_of_nodes(node_genes)
    input_ids = [node_gene.id for node_gene in node_genes if node_gene.is_input()]
    bias_ids = [node_gene.id for node_gene in node_genes if node_gene.is_bias()]

    nn_input = np.zeros((n, 1))
    nn_input[input_ids, :] = input
    nn_input[bias_ids, :] = 1

    return nn_input

def extract_output_vector(node_genes: list[NodeGene], output: np.array) -> np.array:
    output_ids = [node_gene.id for node_gene in node_genes if node_gene.is_output()]

    return output[output_ids, :]

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
