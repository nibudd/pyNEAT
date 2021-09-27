from NodeType import NodeType
import NodeGeneFactory


def test_makes_bias_node():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.type == NodeType.HIDDEN


def test_node_id_is_correct():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.node_id == 0


def test_split_id_is_correct():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.split_id == 0
