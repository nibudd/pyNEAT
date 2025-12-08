import random

from Genotype import Genotype
from GenotypeMutator import GenotypeMutator
from InnovationTracker import InnovationTracker
from NodeGene import InputNodeGene, OutputNodeGene, BiasNodeGene
from StandardConfig import StandardConfig


def make_simple_genotype():
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    return Genotype([in_node, out_node], [])


def test_new_edge_connects_input_to_output(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)
    monkeypatch.setattr(random, "choice", lambda x: x[0])

    result = mutator._mutate_new_edge(genotype)

    assert len(result.edge_genes) == 1
    new_edge = result.edge_genes[0]
    assert new_edge.in_node.id == 0
    assert new_edge.out_node.id == 1


def test_same_connection_twice_returns_same_innovation_id(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)
    monkeypatch.setattr(random, "choice", lambda x: x[0])

    result1 = mutator._mutate_new_edge(genotype)
    result2 = mutator._mutate_new_edge(genotype)

    assert result1.edge_genes[0].innovation_id == result2.edge_genes[0].innovation_id


def test_no_edge_created_when_probability_not_met(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 1.0)

    result = mutator._mutate_new_edge(genotype)

    assert len(result.edge_genes) == 0


def test_edge_source_is_never_output_node(monkeypatch):
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    genotype = Genotype([in_node, out_node], [])
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)
    monkeypatch.setattr(random, "choice", lambda x: x[0])

    result = mutator._mutate_new_edge(genotype)

    for edge in result.edge_genes:
        assert not edge.in_node.is_output()


def test_bias_node_can_be_edge_source(monkeypatch):
    bias_node = BiasNodeGene(0)
    out_node = OutputNodeGene(1)
    genotype = Genotype([bias_node, out_node], [])
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    monkeypatch.setattr(random, "random", lambda: 0.0)
    monkeypatch.setattr(random, "choice", lambda x: x[0])

    result = mutator._mutate_new_edge(genotype)

    assert len(result.edge_genes) == 1
    assert result.edge_genes[0].in_node.id ==  bias_node.id
