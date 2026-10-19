from Hardware.alu import alu_result
from Hardware.arithmetic import int_to_8bit


def test_alu_add():
    result, carry, zero = alu_result(
        int_to_8bit(5),
        int_to_8bit(10),
        (0, 0)
    )

    assert result == int_to_8bit(15)
    assert carry == 0
    assert zero == 0


def test_alu_add_with_carry_and_zero():
    result, carry, zero = alu_result(
        int_to_8bit(255),
        int_to_8bit(1),
        (0, 0)
    )

    assert result == int_to_8bit(0)
    assert carry == 1
    assert zero == 1


def test_alu_and():
    result, carry, zero = alu_result(
        int_to_8bit(15),
        int_to_8bit(51),
        (1, 0)
    )

    assert result == int_to_8bit(3)
    assert carry == 0
    assert zero == 0


def test_alu_or():
    result, carry, zero = alu_result(
        int_to_8bit(15),
        int_to_8bit(51),
        (0, 1)
    )

    assert result == int_to_8bit(63)
    assert carry == 0
    assert zero == 0


def test_alu_xor():
    result, carry, zero = alu_result(
        int_to_8bit(15),
        int_to_8bit(51),
        (1, 1)
    )

    assert result == int_to_8bit(60)
    assert carry == 0
    assert zero == 0


def test_alu_zero_flag_on_logic_operation():
    result, carry, zero = alu_result(
        int_to_8bit(0),
        int_to_8bit(0),
        (1, 0)
    )

    assert result == int_to_8bit(0)
    assert carry == 0
    assert zero == 1