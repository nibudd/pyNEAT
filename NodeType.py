from enum import Enum, auto

class NodeType(Enum):
    BIAS = auto()
    HIDDEN = auto()
    INPUT = auto()
    OUTPUT = auto()

    def is_input(self):
        return (self == self.BIAS) or (self == self.INPUT)