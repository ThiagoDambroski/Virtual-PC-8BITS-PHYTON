import pytest

from Hardware.arithmetic import (
    add_8bit_gate,
    bit8_to_int,
    full_adder_gate,
    half_adder_gate,
    increment_8bit,
    int_to_8bit,
)


def test_int_to_8bit_and_back():
    for value in (0, 1, 5, 127, 128, 255):
        assert bit8_to_int(int_to_8bit(value)) == value


def test_int_to_8bit_rejects_out_of_range_values():
    with pytest.raises(ValueError):
        int_to_8bit(-1)

    with pytest.raises(ValueError):
        int_to_8bit(256)


def test_half_adder():
    assert half_adder_gate(0, 0) == (0, 0)
    assert half_adder_gate(0, 1) == (1, 0)
    assert half_adder_gate(1, 0) == (1, 0)
    assert half_adder_gate(1, 1) == (0, 1)


def test_full_adder():
    assert full_adder_gate(1, 1, 1) == (1, 1)
    assert full_adder_gate(1, 0, 1) == (0, 1)
    assert full_adder_gate(0, 0, 1) == (1, 0)


def test_add_8bit_without_carry():
    result, carry = add_8bit_gate(int_to_8bit(15), int_to_8bit(10))
    assert bit8_to_int(result) == 25
    assert carry == 0


def test_add_8bit_with_carry():
    result, carry = add_8bit_gate(int_to_8bit(255), int_to_8bit(1))
    assert bit8_to_int(result) == 0
    assert carry == 1


def test_increment_8bit():
    result, carry = increment_8bit(int_to_8bit(254))
    assert bit8_to_int(result) == 255
    assert carry == 0

    result, carry = increment_8bit(int_to_8bit(255))
    assert bit8_to_int(result) == 0
    assert carry == 1
