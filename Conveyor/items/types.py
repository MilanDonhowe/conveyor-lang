# Item Types for queues

from enum import Enum, auto, unique


# Enumeration of Item Types
@unique
class  Conv_Type(Enum):
    OPERATOR    = auto()
    INTEGER     = auto()
    STRING      = auto()


BUILTIN_ITEM_OPS = frozenset(["++", "--", "+", "log", "take", "exit", "strcmp", "popn", "pops", "cls", "cln", "ntos", "ston"])

# Item Data-Type
class Conv_Item(object):
    def __init__(self, conv_type, conv_value):
        if (conv_type == Conv_Type.STRING):
            self.VALUE = conv_value.strip("\"")
        else:
            self.VALUE = conv_value
        self.TYPE = conv_type
        
