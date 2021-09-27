from NodeType import NodeType
from NodeGene import NodeGene


def make_bias(node_id: int) -> NodeGene:
    return NodeGene(NodeType.BIAS, node_id)


def make_hidden(node_id: int, split_id: int) -> NodeGene:
    return NodeGene(NodeType.HIDDEN, node_id, split_id)


def make_input(node_id: int) -> NodeGene:
    return NodeGene(NodeType.INPUT, node_id)


def make_output(node_id: int) -> NodeGene:
    return NodeGene(NodeType.OUTPUT, node_id)
