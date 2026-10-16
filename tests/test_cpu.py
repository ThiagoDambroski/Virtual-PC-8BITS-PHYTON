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
