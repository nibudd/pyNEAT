import NodeGeneFactory


def test_makes_input_node():
    node_gene = NodeGeneFactory.make_input(0)

    assert node_gene.is_input()


def test_node_id_is_correct():
    node_gene = NodeGeneFactory.make_input(0)

    assert node_gene.node_id == 0
