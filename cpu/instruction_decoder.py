from Hardware.arithmetic import equal_8bit
from Hardware.bit_types import Bit,Bits8
from cpu.instruction_set import LOAD_IMMEDIATE_OPCODE, ADD_OPCODE


def decode_instruction(opcode:Bits8) -> tuple[Bit, Bit]:
    is_load:Bit = equal_8bit(opcode,LOAD_IMMEDIATE_OPCODE)
    is_add:Bit = equal_8bit(opcode,ADD_OPCODE)
    return is_load,is_add