from NodeType import NodeType

class NodeGene:

    def __init__(self, node_type: NodeType, id: int):
        self.type = node_type
        self.id = id

    def is_bias(self) -> bool:
        return self.type == NodeType.BIAS

    def is_input(self) -> bool:
        return self.type == NodeType.INPUT

    def is_output(self) -> bool:
        return self.type == NodeType.OUTPUT