from NodeType import NodeType
from NodeGene import NodeGene

def make_bias(id: int) -> NodeGene:
    return NodeGene(NodeType.BIAS, id)

def make_hidden(id: int, split_id: int) -> NodeGene:
    return NodeGene(NodeType.HIDDEN, id, split_id)

def make_input(id: int) -> NodeGene:
    return NodeGene(NodeType.INPUT, id)

def make_output(id: int) -> NodeGene:
    return NodeGene(NodeType.OUTPUT, id)