import pytest
from NodeType import NodeType


@pytest.mark.parametrize("node_type,expected", [
    (NodeType.BIAS, True),
    (NodeType.HIDDEN, False),
    (NodeType.INPUT, True),
    (NodeType.OUTPUT, False)
])
def test_is_input(node_type: NodeType, expected: bool):
    assert expected == node_type.is_input()

@pytest.mark.parametrize("node_type,expected", [
    (NodeType.BIAS, False),
    (NodeType.HIDDEN, False),
    (NodeType.INPUT, False),
    (NodeType.OUTPUT, True)
])
def test_is_output(node_type: NodeType, expected: bool):
    assert expected == node_type.is_output()