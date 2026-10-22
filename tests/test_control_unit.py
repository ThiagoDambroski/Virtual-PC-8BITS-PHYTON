from Hardware.arithmetic import int_to_8bit
from Hardware.memory import Ram256
from cpu.control_unit import execute_load_immediate
from cpu.program_counter import ProgramCounter
from cpu.registers import RegisterBank


def test_execute_load_immediate_r2():
    ram = Ram256()
    pc = ProgramCounter()
    registers = RegisterBank()

    ram.write(1, int_to_8bit(0), int_to_8bit(0x02))
    ram.write(1, int_to_8bit(1), int_to_8bit(0x02))
    ram.write(1, int_to_8bit(2), int_to_8bit(42))

    pc.increment()

    execute_load_immediate(ram, pc, registers)

    assert registers.read((0, 1)) == int_to_8bit(42)
    assert pc.read() == int_to_8bit(3)


def test_execute_load_immediate_r0():
    ram = Ram256()
    pc = ProgramCounter()
    registers = RegisterBank()

    ram.write(1, int_to_8bit(0), int_to_8bit(0x00))
    ram.write(1, int_to_8bit(1), int_to_8bit(99))

    execute_load_immediate(ram, pc, registers)

    assert registers.read((0, 0)) == int_to_8bit(99)
    assert pc.read() == int_to_8bit(2)


def test_execute_load_immediate_only_changes_selected_register():
    ram = Ram256()
    pc = ProgramCounter()
    registers = RegisterBank()

    registers.write((0, 0), int_to_8bit(10))
    registers.write((1, 0), int_to_8bit(20))
    registers.write((0, 1), int_to_8bit(30))
    registers.write((1, 1), int_to_8bit(40))

    ram.write(1, int_to_8bit(0), int_to_8bit(0x01))
    ram.write(1, int_to_8bit(1), int_to_8bit(77))

    execute_load_immediate(ram, pc, registers)

    assert registers.read((0, 0)) == int_to_8bit(10)
    assert registers.read((1, 0)) == int_to_8bit(77)
    assert registers.read((0, 1)) == int_to_8bit(30)
    assert registers.read((1, 1)) == int_to_8bit(40)