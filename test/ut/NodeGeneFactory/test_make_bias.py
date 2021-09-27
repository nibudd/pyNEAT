import NodeGeneFactory


def test_makes_bias_node():
    node_gene = NodeGeneFactory.make_bias(0)

    assert node_gene.is_bias()


def test_node_id_is_correct():
    node_gene = NodeGeneFactory.make_bias(0)

    assert node_gene.node_id == 0
