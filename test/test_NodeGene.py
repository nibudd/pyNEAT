import pytest
from NodeGene import NodeGene
from NodeType import NodeType


@pytest.mark.parametrize("node_type,expected", [
    (NodeType.BIAS, True),
    (NodeType.HIDDEN, False),
    (NodeType.INPUT, True),
    (NodeType.OUTPUT, False)
])
def test_is_input(node_type: NodeType, expected: bool):
    node_gene = NodeGene(node_type, 0)

    assert expected == node_gene.is_input()

@pytest.mark.parametrize("node_type,expected", [
    (NodeType.BIAS, False),
    (NodeType.HIDDEN, False),
    (NodeType.INPUT, False),
    (NodeType.OUTPUT, True)
])
def test_is_output(node_type: NodeType, expected: bool):
    node_gene = NodeGene(node_type, 0)

    assert expected == node_gene.is_output()