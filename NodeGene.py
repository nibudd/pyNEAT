from NodeType import NodeType


class NodeGene:

    def __init__(self, node_type: NodeType, node_id: int, split_id: int = None):
        self.type = node_type
        self.node_id = node_id
        self.split_id = split_id

    def is_bias(self) -> bool:
        return self.type == NodeType.BIAS

    def is_input(self) -> bool:
        return self.type == NodeType.INPUT

    def is_output(self) -> bool:
        return self.type == NodeType.OUTPUT
