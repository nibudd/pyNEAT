from NodeGene import NodeGene
from NodeType import NodeType
import NodeGeneFactory

def test_makeBias_makesBiasNode():
    node_gene = NodeGeneFactory.make_bias(0)

    assert node_gene.is_bias()


def test_makeBias_idIsCorrect():
    node_gene = NodeGeneFactory.make_bias(0)

    assert node_gene.id == 0


def test_makeHidden_makesBiasNode():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.type == NodeType.HIDDEN


def test_makeHidden_idIsCorrect():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.id == 0

def test_makeHidden_splitIdIsCorrect():
    node_gene = NodeGeneFactory.make_hidden(0, 0)

    assert node_gene.split_id == 0

def test_makeInput_makesInputNode():
    node_gene = NodeGeneFactory.make_input(0)

    assert node_gene.is_input()


def test_makeInput_idIsCorrect():
    node_gene = NodeGeneFactory.make_input(0)

    assert node_gene.id == 0

def test_makeOutput_makesOutputNode():
    node_gene = NodeGeneFactory.make_output(0)

    assert node_gene.is_output()


def test_makeOutput_idIsCorrect():
    node_gene = NodeGeneFactory.make_output(0)

    assert node_gene.id == 0