import pytest
from NodeGene import NodeGene
from NodeType import NodeType


@pytest.mark.parametrize("node_type,expected", [
    (NodeType.BIAS, True),
    (NodeType.HIDDEN, False),
    (NodeType.INPUT, False),
    (NodeType.OUTPUT, False)
])
def test(node_type: NodeType, expected: bool):
    node_gene = NodeGene(node_type, 0)

    assert expected == node_gene.is_bias()
