from Hardware.arithmetic import int_to_8bit
from Hardware.gates import (
    and_gate,
    dmux4way_gate,
    dmux_gate,
    mux4way8bit_gate,
    mux_gate,
    mux_gate8bit,
    nand,
    not_gate,
    or_gate,
    xor_gate,
)


def test_nand_truth_table():
    assert nand(0, 0) == 1
    assert nand(0, 1) == 1
    assert nand(1, 0) == 1
    assert nand(1, 1) == 0


def test_not_gate():
    assert not_gate(0) == 1
    assert not_gate(1) == 0


def test_and_gate():
    assert and_gate(0, 0) == 0
    assert and_gate(0, 1) == 0
    assert and_gate(1, 0) == 0
    assert and_gate(1, 1) == 1


def test_or_gate():
    assert or_gate(0, 0) == 0
    assert or_gate(0, 1) == 1
    assert or_gate(1, 0) == 1
    assert or_gate(1, 1) == 1


def test_xor_gate():
    assert xor_gate(0, 0) == 0
    assert xor_gate(0, 1) == 1
    assert xor_gate(1, 0) == 1
    assert xor_gate(1, 1) == 0


def test_mux_gate():
    assert mux_gate(0, 1, 0) == 0
    assert mux_gate(0, 1, 1) == 1


def test_mux_gate8bit():
    a = int_to_8bit(5)
    b = int_to_8bit(10)
    assert mux_gate8bit(0, a, b) == a
    assert mux_gate8bit(1, a, b) == b


def test_dmux_gate():
    assert dmux_gate(0, 1) == (1, 0)
    assert dmux_gate(1, 1) == (0, 1)
    assert dmux_gate(0, 0) == (0, 0)
    assert dmux_gate(1, 0) == (0, 0)


def test_dmux4way_gate():
    assert dmux4way_gate((0, 0), 1) == (1, 0, 0, 0)
    assert dmux4way_gate((1, 0), 1) == (0, 1, 0, 0)
    assert dmux4way_gate((0, 1), 1) == (0, 0, 1, 0)
    assert dmux4way_gate((1, 1), 1) == (0, 0, 0, 1)
    assert dmux4way_gate((1, 1), 0) == (0, 0, 0, 0)


def test_mux4way8bit_gate():
    a = int_to_8bit(10)
    b = int_to_8bit(20)
    c = int_to_8bit(30)
    d = int_to_8bit(40)
    assert mux4way8bit_gate((0, 0), a, b, c, d) == a
    assert mux4way8bit_gate((1, 0), a, b, c, d) == b
    assert mux4way8bit_gate((0, 1), a, b, c, d) == c
    assert mux4way8bit_gate((1, 1), a, b, c, d) == d


from Hardware.arithmetic import int_to_8bit,equal_8bit


def test_equal_8bit_equal_values():
    assert equal_8bit(int_to_8bit(0), int_to_8bit(0)) == 1
    assert equal_8bit(int_to_8bit(2), int_to_8bit(2)) == 1
    assert equal_8bit(int_to_8bit(255), int_to_8bit(255)) == 1


def test_equal_8bit_different_values():
    assert equal_8bit(int_to_8bit(2), int_to_8bit(3)) == 0
    assert equal_8bit(int_to_8bit(0), int_to_8bit(255)) == 0
    assert equal_8bit(int_to_8bit(127), int_to_8bit(128)) == 0


def test_equal_8bit_single_bit_difference():
    assert equal_8bit(
        (0, 0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0, 0)
    ) == 0