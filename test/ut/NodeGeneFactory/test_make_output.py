import NodeGeneFactory


def test_makes_output_node():
    node_gene = NodeGeneFactory.make_output(0)

    assert node_gene.is_output()


def test_node_id_is_correct():
    node_gene = NodeGeneFactory.make_output(0)

    assert node_gene.node_id == 0
