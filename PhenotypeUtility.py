from collections import deque
from typing import Callable, List
import numpy as np

from NodeGene import NodeGene
from Genotype import Genotype


def evaluate_feedforward(genotype: Genotype, inputs: np.array, transfer_function: Callable) -> np.array:
    """Single forward pass through a feedforward network."""
    node_values = _initialize_node_values(genotype, inputs)
    incoming_edges = _build_incoming_edges_map(genotype)
    sorted_nodes = _topological_sort(genotype)

    for node in sorted_nodes:
        if node.is_input() or node.is_bias():
            continue

        weighted_sum = sum(
            edge.weight * node_values[edge.in_node.id]
            for edge in incoming_edges[node.id]
        )
        node_values[node.id] = transfer_function(weighted_sum)

    return _extract_outputs(genotype, node_values)


def _initialize_node_values(genotype: Genotype, inputs: np.array) -> dict:
    """Set initial values: inputs from array, bias=1, others=0."""
    node_values = {}
    input_idx = 0

    for node in genotype.node_genes:
        if node.is_input():
            node_values[node.id] = float(inputs[input_idx])
            input_idx += 1
        elif node.is_bias():
            node_values[node.id] = 1.0
        else:
            node_values[node.id] = 0.0

    return node_values


def _build_incoming_edges_map(genotype: Genotype) -> dict:
    """Map each node to its incoming enabled edges."""
    incoming = {node.id: [] for node in genotype.node_genes}
    for edge in genotype.edge_genes:
        if edge.enabled:
            incoming[edge.out_node.id].append(edge)
    return incoming


def _topological_sort(genotype: Genotype) -> List[NodeGene]:
    """Kahn's algorithm - returns nodes in dependency order."""
    node_map = {node.id: node for node in genotype.node_genes}
    in_degree = {node.id: 0 for node in genotype.node_genes}
    adjacency = {node.id: [] for node in genotype.node_genes}

    for edge in genotype.edge_genes:
        if edge.enabled:
            adjacency[edge.in_node.id].append(edge.out_node.id)
            in_degree[edge.out_node.id] += 1

    queue = deque(node for node in genotype.node_genes if in_degree[node.id] == 0)
    sorted_nodes = []

    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        for neighbor_id in adjacency[node.id]:
            in_degree[neighbor_id] -= 1
            if in_degree[neighbor_id] == 0:
                queue.append(node_map[neighbor_id])

    return sorted_nodes


def _extract_outputs(genotype: Genotype, node_values: dict) -> np.array:
    """Return output node values as column vector."""
    outputs = [node_values[node.id] for node in genotype.node_genes if node.is_output()]
    return np.array([outputs]).T
