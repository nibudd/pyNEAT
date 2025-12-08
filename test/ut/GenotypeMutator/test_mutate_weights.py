import random

from EdgeGene import EdgeGene
from Genotype import Genotype
from GenotypeMutator import GenotypeMutator
from InnovationTracker import InnovationTracker
from NodeGene import InputNodeGene, OutputNodeGene
from StandardConfig import StandardConfig


def make_simple_genotype():
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge = EdgeGene(0, 0, in_node, out_node, 0.5, True)
    return Genotype([in_node, out_node], [edge])


def test_weight_perturbation_stays_within_limits(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # Force mutation to happen (rand=0 <= 0.8) and perturb (rand=0 <= 0.9)
    values = iter([0.0, 0.0, 0.5])
    monkeypatch.setattr(random, "random", lambda: next(values))

    result = mutator._mutate_weights(genotype)

    original_weight = 0.5
    perturbation = (
        0.5 * 2 * StandardConfig.weight_perturbation_limit
        - StandardConfig.weight_perturbation_limit
    )
    expected = original_weight + perturbation
    assert result.edge_genes[0].weight == expected


def test_weight_reset_gives_value_within_limits(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # Force mutation (rand=0) but not perturb (rand=1 > 0.9), then reset with rand=0.5
    values = iter([0.0, 1.0, 0.5])
    monkeypatch.setattr(random, "random", lambda: next(values))

    result = mutator._mutate_weights(genotype)

    expected = (
        0.5 * 2 * StandardConfig.weight_reset_limit - StandardConfig.weight_reset_limit
    )
    assert result.edge_genes[0].weight == expected


def test_disabled_gene_can_be_reenabled(monkeypatch):
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge = EdgeGene(0, 0, in_node, out_node, 0.5, False)
    genotype = Genotype([in_node, out_node], [edge])
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # Skip weight mutation (rand=1 > 0.8), then reenable (rand=0 <= 0.25)
    values = iter([1.0, 0.0])
    monkeypatch.setattr(random, "random", lambda: next(values))

    result = mutator._mutate_weights(genotype)

    assert result.edge_genes[0].enabled is True


def test_enabled_gene_stays_enabled(monkeypatch):
    genotype = make_simple_genotype()
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    # Skip weight mutation (rand=1 > 0.8)
    monkeypatch.setattr(random, "random", lambda: 1.0)

    result = mutator._mutate_weights(genotype)

    assert result.edge_genes[0].enabled is True


def test_original_genotype_is_not_modified(monkeypatch):
    genotype = make_simple_genotype()
    original_weight = genotype.edge_genes[0].weight
    tracker = InnovationTracker(1, 0, 0)
    mutator = GenotypeMutator(StandardConfig, tracker)

    values = iter([0.0, 0.0, 0.5])
    monkeypatch.setattr(random, "random", lambda: next(values))

    mutator._mutate_weights(genotype)

    assert genotype.edge_genes[0].weight == original_weight
