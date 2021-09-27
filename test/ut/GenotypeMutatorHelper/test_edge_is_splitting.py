import pytest
from GenotypeMutatorHelper import GenotypeMutatorHelper
from StandardConfig import StandardConfig


@pytest.mark.parametrize("random_value,expected", [
    (0, True),
    (.2, True),
    (.5, True),
    (.51, False),
    (.8, False),
    (1, False)
])
def test_returns_correct_value(random_value: float, expected: bool):
    config = StandardConfig()
    config.chance_of_adding_new_node = 0.5

    helper = GenotypeMutatorHelper(config, 1)

    assert expected == helper.edge_is_splitting(random_value)
