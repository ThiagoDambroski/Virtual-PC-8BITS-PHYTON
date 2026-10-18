from typing import cast

from Hardware.bit_types import Bit, Bits2, Bits8
from Hardware.gates import and_gate, or_gate, xor_gate,not_gate


def int_to_8bit(a: int) -> Bits8:
    if not 0 <= a <= 0xFF:
        raise ValueError("Value must be between 0 and 255")

    return (
        1 if (a >> 0) & 1 else 0,
        1 if (a >> 1) & 1 else 0,
        1 if (a >> 2) & 1 else 0,
        1 if (a >> 3) & 1 else 0,
        1 if (a >> 4) & 1 else 0,
        1 if (a >> 5) & 1 else 0,
        1 if (a >> 6) & 1 else 0,
        1 if (a >> 7) & 1 else 0,
    )


def bit8_to_int(bits8: Bits8) -> int:
    total = 0

    for i in range(8):
        total |= bits8[i] << i

    return total


def half_adder_gate(a: Bit, b: Bit) -> Bits2:
    sum_bit = xor_gate(a, b)
    carry = and_gate(a, b)
    return sum_bit, carry


def full_adder_gate(a: Bit, b: Bit, carry_in: Bit) -> Bits2:
    partial_sum, first_carry = half_adder_gate(a, b)
    sum_bit, second_carry = half_adder_gate(partial_sum, carry_in)
    carry_out = or_gate(first_carry, second_carry)
    return sum_bit, carry_out


def add_8bit_gate(a: Bits8, b: Bits8) -> tuple[Bits8, Bit]:
    out_list: list[Bit] = []

    sum_bit, internal_carry = half_adder_gate(a[0], b[0])
    out_list.append(sum_bit)

    for i in range(1, 8):
        sum_bit, internal_carry = full_adder_gate(a[i], b[i], internal_carry)
        out_list.append(sum_bit)

    return cast(Bits8, tuple(out_list)), internal_carry


def add_from_int(a: int, b: int) -> tuple[int, Bit]:
    sum_bits, carry_out = add_8bit_gate(int_to_8bit(a), int_to_8bit(b))
    return bit8_to_int(sum_bits), carry_out


def increment_8bit(a: Bits8) -> tuple[Bits8, Bit]:
    return add_8bit_gate(a, int_to_8bit(1))


def is_zero_8bit(value:Bits8) -> Bit:
    has_one =  0
    for i in range(8):
        has_one = or_gate(has_one,value[i])

    return not_gate(has_one)

def add_8bit_with_flags(a: Bits8, b: Bits8) -> tuple[Bits8, Bit,Bit]:
    result,carry = add_8bit_gate(a, b)
    return result,carry,is_zero_8bit(result)
