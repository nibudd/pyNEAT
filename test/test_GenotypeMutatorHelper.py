import numpy as np

from GenotypeMutatorHelper import GenotypeMutatorHelper
from StandardConfig import StandardConfig


def test_weightIsMutating_chanceOfWeightMutatingIs1_returnsTrue():
    config = StandardConfig()
    config.chance_of_weight_mutating = 1.0

    helper = GenotypeMutatorHelper(config, 1)

    assert helper.weight_is_mutating()


def test_weightIsMutating_chanceOfWeightMutatingIs0_returnsFalse():
    config = StandardConfig()
    config.chance_of_weight_mutating = 0.0

    helper = GenotypeMutatorHelper(config, 1)

    assert not helper.weight_is_mutating()

def test_weightIsPerturbing_chanceOfWeightPerturbingIs1_returnsTrue():
    config = StandardConfig()
    config.chance_of_weight_perturbing = 1.0

    helper = GenotypeMutatorHelper(config, 1)

    assert helper.weight_is_perturbing()


def test_weightIsPerturbing_chanceOfWeightPerturbingIs0_returnsFalse():
    config = StandardConfig()
    config.chance_of_weight_perturbing = 0.0

    helper = GenotypeMutatorHelper(config, 1)

    assert not helper.weight_is_perturbing()

def test_geneIsReenabling_chanceOfEnablingDisabledGeneIs1_returnsTrue():
    config = StandardConfig()
    config.chance_of_enabling_disabled_gene = 1.0

    helper = GenotypeMutatorHelper(config, 1)

    assert helper.gene_is_reenabling()


def test_geneIsReenabling_chanceOfEnablingDisabledGeneIs0_returnsFalse():
    config = StandardConfig()
    config.chance_of_enabling_disabled_gene = 0.0

    helper = GenotypeMutatorHelper(config, 1)

    assert not helper.gene_is_reenabling()

def test_edgeIsSplitting_chanceOfAddingNewNodeIs1_returnsTrue():
    config = StandardConfig()
    config.chance_of_adding_new_node = 1.0

    helper = GenotypeMutatorHelper(config, 1)

    assert helper.edge_is_splitting()


def test_edgeIsSplitting_chanceOfAddingNewNodeIs0_returnsFalse():
    config = StandardConfig()
    config.chance_of_adding_new_node = 0.0

    helper = GenotypeMutatorHelper(config, 1)

    assert not helper.edge_is_splitting()

def test_newEdgeIsBeingAdded_chanceOfAddingNewEdgeIs1_returnsTrue():
    config = StandardConfig()
    config.chance_of_adding_new_edge = 1.0

    helper = GenotypeMutatorHelper(config, 1)

    assert helper.new_edge_is_being_added()


def test_newEdgeIsBeingAdded_chanceOfAddingNewEdgeIs0_returnsFalse():
    config = StandardConfig()
    config.chance_of_adding_new_edge = 0.0

    helper = GenotypeMutatorHelper(config, 1)

    assert not helper.new_edge_is_being_added()

# todo: still need to add tests for perturb_weight() and downward