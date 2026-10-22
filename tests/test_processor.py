from Hardware.arithmetic import int_to_8bit
from Hardware.memory import Ram256
from cpu.instruction_register import InstructionRegister
from cpu.processor import fetch_opcode
from cpu.program_counter import ProgramCounter


def test_fetch_opcode_loads_instruction_register():
    ram = Ram256()
    pc = ProgramCounter()
    instruction_register = InstructionRegister()

    ram.write(
        1,
        int_to_8bit(0),
        int_to_8bit(0x02)
    )

    fetch_opcode(ram, pc, instruction_register)

    assert instruction_register.read() == int_to_8bit(0x02)


def test_fetch_opcode_increments_program_counter():
    ram = Ram256()
    pc = ProgramCounter()
    instruction_register = InstructionRegister()

    ram.write(
        1,
        int_to_8bit(0),
        int_to_8bit(0x02)
    )

    fetch_opcode(ram, pc, instruction_register)

    assert pc.read() == int_to_8bit(1)


def test_fetch_opcode_reads_next_instruction():
    ram = Ram256()
    pc = ProgramCounter()
    instruction_register = InstructionRegister()

    ram.write(1, int_to_8bit(0), int_to_8bit(0x02))
    ram.write(1, int_to_8bit(1), int_to_8bit(0x03))

    fetch_opcode(ram, pc, instruction_register)

    assert instruction_register.read() == int_to_8bit(0x02)

    fetch_opcode(ram, pc, instruction_register)

    assert instruction_register.read() == int_to_8bit(0x03)
    assert pc.read() == int_to_8bit(2)