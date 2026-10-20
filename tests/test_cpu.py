import pytest

from Hardware.arithmetic import bit8_to_int, int_to_8bit
from Hardware.memory import Ram256
from cpu.processor import fetch
from cpu.program_counter import ProgramCounter


def test_program_counter_starts_at_zero():
    pc = ProgramCounter()
    assert bit8_to_int(pc.read()) == 0


def test_program_counter_increments_and_wraps():
    pc = ProgramCounter()

    for expected in range(256):
        assert bit8_to_int(pc.read()) == expected
        pc.increment()

    assert bit8_to_int(pc.read()) == 0


def test_fetch_reads_current_address_and_increments_pc():
    ram = Ram256()
    pc = ProgramCounter()

    ram.write(1, int_to_8bit(0), int_to_8bit(42))
    ram.write(1, int_to_8bit(1), int_to_8bit(99))

    assert bit8_to_int(fetch(ram, pc)) == 42
    assert bit8_to_int(pc.read()) == 1

    assert bit8_to_int(fetch(ram, pc)) == 99
    assert bit8_to_int(pc.read()) == 2

from cpu.instruction_register import InstructionRegister


def test_instruction_register():
    instruction_register = InstructionRegister()

    assert instruction_register.read() == int_to_8bit(0)

    instruction_register.load(int_to_8bit(0x02))
    assert instruction_register.read() == int_to_8bit(0x02)

    instruction_register.load(int_to_8bit(0x03))
    assert instruction_register.read() == int_to_8bit(0x03)

from Hardware.arithmetic import int_to_8bit
from cpu.instruction_decoder import decode_instruction


def test_decode_load():
    is_load, is_add = decode_instruction(int_to_8bit(0x02))

    assert is_load == 1
    assert is_add == 0


def test_decode_add():
    is_load, is_add = decode_instruction(int_to_8bit(0x03))

    assert is_load == 0
    assert is_add == 1


def test_decode_unknown_opcode():
    is_load, is_add = decode_instruction(int_to_8bit(0xFF))

    assert is_load == 0
    assert is_add == 0

from cpu.register_decoder import decode_register


def test_decode_r0():
    assert decode_register(int_to_8bit(0x00)) == (0, 0)


def test_decode_r1():
    assert decode_register(int_to_8bit(0x01)) == (1, 0)


def test_decode_r2():
    assert decode_register(int_to_8bit(0x02)) == (0, 1)


def test_decode_r3():
    assert decode_register(int_to_8bit(0x03)) == (1, 1)


def test_reject_invalid_register():
    with pytest.raises(ValueError):
        decode_register(int_to_8bit(0x04))


def test_reject_large_invalid_register():
    with pytest.raises(ValueError):
        decode_register(int_to_8bit(0xFF))