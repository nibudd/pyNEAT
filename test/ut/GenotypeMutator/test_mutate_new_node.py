import random

from EdgeGene import EdgeGene
from Genotype import Genotype
from GenotypeMutator import GenotypeMutator
from InnovationTracker import InnovationTracker
from NodeGene import InputNodeGene, OutputNodeGene, HiddenNodeGene
from StandardConfig import StandardConfig


def make_simple_genotype():
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge = EdgeGene(0, 0, in_node, out_node, 0.5, True)
    return Genotype([in_node, out_node], [edge])


def test_splitting_edge_creates_new_hidden_node(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # Force split (rand=0 <= 0.03)
    monkeypatch.setattr(random, "random", lambda: 0.0)

    result = mutator._mutate_new_node(genotype)

    assert len(result.node_genes) == 3
    new_node = result.node_genes[2]
    assert isinstance(new_node, HiddenNodeGene)
    assert new_node.id == 2


def test_splitting_edge_creates_two_new_edges(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)

    result = mutator._mutate_new_node(genotype)

    assert len(result.edge_genes) == 3
    new_start_edge = result.edge_genes[1]
    new_end_edge = result.edge_genes[2]
    assert new_start_edge.id == 1
    assert new_end_edge.id == 2


def test_original_edge_is_disabled_after_split(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)

    result = mutator._mutate_new_node(genotype)

    assert result.edge_genes[0].enabled is False


def test_new_edges_have_correct_weights(monkeypatch):
    genotype = make_simple_genotype()
    original_weight = genotype.edge_genes[0].weight
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)

    result = mutator._mutate_new_node(genotype)

    new_start_edge = result.edge_genes[1]
    new_end_edge = result.edge_genes[2]
    assert new_start_edge.weight == 1.0
    assert new_end_edge.weight == original_weight


def test_same_edge_split_twice_returns_same_node_id(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)

    result1 = mutator._mutate_new_node(genotype)
    result2 = mutator._mutate_new_node(genotype)

    new_node1 = result1.node_genes[2]
    new_node2 = result2.node_genes[2]
    assert new_node1.id == new_node2.id


def test_no_split_when_probability_not_met(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # rand=1 > 0.03, no split
    monkeypatch.setattr(random, "random", lambda: 1.0)

    result = mutator._mutate_new_node(genotype)

    assert len(result.node_genes) == 2
    assert len(result.edge_genes) == 1
