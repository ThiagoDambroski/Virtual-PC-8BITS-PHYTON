from Hardware.arithmetic import add_8bit_gate, is_zero_8bit
from Hardware.bit_types import Bit, Bits2, Bits8
from Hardware.gates import (
    and_gate_8bits,
    or_gate_8bits,
    xor_gate_8bits,
    mux4way8bit_gate, not_gate, and_gate
)
#opcode:
#(0, 0) → ADD
#(1, 0) → AND
#(0, 1) → OR
#(1, 1) → XOR

def alu_result(a: Bits8, b: Bits8, operation: Bits2) -> tuple[Bits8, Bit,Bit]:
    add_result, add_carry = add_8bit_gate(a, b)
    and_result = and_gate_8bits(a, b)
    or_result = or_gate_8bits(a, b)
    xor_result = xor_gate_8bits(a, b)
    result = mux4way8bit_gate(operation, add_result, and_result, or_result, xor_result)
    is_add = and_gate(not_gate(operation[0]),not_gate(operation[1]))
    carry = and_gate(add_carry,is_add)
    zero = is_zero_8bit(result)
    return result,carry,zero