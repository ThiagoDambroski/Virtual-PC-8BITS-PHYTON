from typing import cast

from Hardware.bit_types import Bit, Bits2, Bits4, Bits8


def nand(a: Bit, b: Bit) -> Bit:
    return 0 if a and b else 1


def not_gate(a: Bit) -> Bit:
    return nand(a, a)


def and_gate(a: Bit, b: Bit) -> Bit:
    return not_gate(nand(a, b))


def or_gate(a: Bit, b: Bit) -> Bit:
    return nand(not_gate(a), not_gate(b))


def xor_gate(a: Bit, b: Bit) -> Bit:
    return and_gate(or_gate(a, b), nand(a, b))


def mux_gate(a: Bit, b: Bit, sel: Bit) -> Bit:
    not_sel = not_gate(sel)
    first_gate = and_gate(a, not_sel)
    second_gate = and_gate(b, sel)
    return or_gate(first_gate, second_gate)


def mux_gate8bit(sel: Bit, a: Bits8, b: Bits8) -> Bits8:
    out_list: list[Bit] = []

    for i in range(8):
        out_list.append(mux_gate(a[i], b[i], sel))

    return cast(Bits8, tuple(out_list))


def dmux_gate(sel: Bit, load: Bit) -> Bits2:
    return_a = and_gate(not_gate(sel), load)
    return_b = and_gate(sel, load)
    return return_a, return_b


def dmux4way_gate(sel: Bits2, load: Bit) -> Bits4:
    active_first, active_second = dmux_gate(sel[1], load)
    return_a, return_b = dmux_gate(sel[0], active_first)
    return_c, return_d = dmux_gate(sel[0], active_second)
    return return_a, return_b, return_c, return_d


def mux4way8bit_gate(
    sel: Bits2,
    a: Bits8,
    b: Bits8,
    c: Bits8,
    d: Bits8,
) -> Bits8:
    first = mux_gate8bit(sel[0], a, b)
    second = mux_gate8bit(sel[0], c, d)
    return mux_gate8bit(sel[1], first, second)
