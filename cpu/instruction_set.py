from Hardware.arithmetic import int_to_8bit
from Hardware.bit_types import Bits8

LOAD_IMMEDIATE_OPCODE:Bits8 = int_to_8bit(2)
ADD_OPCODE:Bits8 = int_to_8bit(3)