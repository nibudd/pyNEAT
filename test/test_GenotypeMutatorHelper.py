import pytest

from GenotypeMutatorHelper import GenotypeMutatorHelper
from StandardConfig import StandardConfig


parametrized_values = [
    (0, True),
    (.2, True),
    (.5, True),
    (.51, False),
    (.8, False),
    (1, False)
]

@pytest.mark.parametrize("input,expected", parametrized_values)
def test_weightIsMutating_returnsCorrectValue(input: float, expected: bool):
    config = StandardConfig()
    config.chance_of_weight_mutating = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.weight_is_mutating(input)

@pytest.mark.parametrize("input,expected", parametrized_values)
def test_weightIsPerturbing_returnsCorrectValue(input: float, expected: bool):
    config = StandardConfig()
    config.chance_of_weight_perturbing = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.weight_is_perturbing(input)

@pytest.mark.parametrize("input,expected", parametrized_values)
def test_geneIsReenabling_returnsCorrectValue(input: float, expected: bool):
    config = StandardConfig()
    config.chance_of_enabling_disabled_gene = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.gene_is_reenabling(input)

@pytest.mark.parametrize("input,expected", parametrized_values)
def test_edgeIsSplitting_returnsCorrectValue(input: float, expected: bool):
    config = StandardConfig()
    config.chance_of_adding_new_node = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.edge_is_splitting(input)

@pytest.mark.parametrize("input,expected", parametrized_values)
def test_newEdgeIsBeingAdded_returnsCorrectValue(input: float, expected: bool):
    config = StandardConfig()
    config.chance_of_adding_new_edge = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.new_edge_is_being_added(input)

# todo: still need to add tests for perturb_weight() and downward