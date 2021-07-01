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
