from EdgeGene import EdgeGene
from Genotype import Genotype
from GenotypeMutator import GenotypeMutator
from NodeGene import InputNodeGene, OutputNodeGene, BiasNodeGene
from StandardConfig import StandardConfig


def test_sets_last_node_id_to_max_node_id():
    node1 = InputNodeGene(1)
    node2 = InputNodeGene(5)
    node3 = OutputNodeGene(3)
    genotype = Genotype([node1, node2, node3], [])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_node_id == 5


def test_sets_last_node_id_to_zero_when_no_nodes():
    genotype = Genotype([], [])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_node_id == 0


def test_sets_last_edge_id_to_max_edge_id():
    node1 = InputNodeGene(1)
    node2 = OutputNodeGene(2)
    edge1 = EdgeGene(3, 100, node1, node2, 0.5, True)
    edge2 = EdgeGene(7, 101, node1, node2, 0.5, True)
    edge3 = EdgeGene(5, 102, node1, node2, 0.5, True)
    genotype = Genotype([node1, node2], [edge1, edge2, edge3])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_edge_id == 7


def test_sets_last_edge_id_to_zero_when_no_edges():
    node1 = InputNodeGene(1)
    genotype = Genotype([node1], [])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_edge_id == 0


def test_sets_last_innovation_id_to_max_innovation_id():
    node1 = InputNodeGene(1)
    node2 = OutputNodeGene(2)
    edge1 = EdgeGene(1, 10, node1, node2, 0.5, True)
    edge2 = EdgeGene(2, 25, node1, node2, 0.5, True)
    edge3 = EdgeGene(3, 15, node1, node2, 0.5, True)
    genotype = Genotype([node1, node2], [edge1, edge2, edge3])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_innovation_id == 25


def test_sets_last_innovation_id_to_zero_when_no_edges():
    node1 = InputNodeGene(1)
    genotype = Genotype([node1], [])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_innovation_id == 0


def test_handles_single_node():
    node1 = BiasNodeGene(42)
    genotype = Genotype([node1], [])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_node_id == 42


def test_handles_single_edge():
    node1 = InputNodeGene(1)
    node2 = OutputNodeGene(2)
    edge = EdgeGene(99, 50, node1, node2, 0.5, True)
    genotype = Genotype([node1, node2], [edge])

    mutator = GenotypeMutator(genotype, StandardConfig)

    assert mutator.last_edge_id == 99
    assert mutator.last_innovation_id == 50
