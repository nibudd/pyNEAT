from enum import Enum, auto


class NodeType(Enum):
    BIAS = auto()
    HIDDEN = auto()
    INPUT = auto()
    OUTPUT = auto()
