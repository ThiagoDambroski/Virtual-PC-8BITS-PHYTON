from Hardware.arithmetic import int_to_8bit, bit8_to_int
from Hardware.memory import Ram256
from cpu.program_counter import ProgramCounter
from cpu.instruction_register import InstructionRegister
from cpu.registers import RegisterBank
from cpu.cpu_core import step,run


def test_load_immediate():
    ram = Ram256()
    pc = ProgramCounter()
    ir = InstructionRegister()

    ram.write(1,int_to_8bit(0),int_to_8bit(2)) #opcode
    ram.write(1,int_to_8bit(1),int_to_8bit(2)) #register
    ram.write(1,int_to_8bit(2),int_to_8bit(20)) #value

    registers = RegisterBank()
    step(ram,pc,ir,registers)

    assert bit8_to_int(registers.read((0,1))) == 20 #register 2 LSB
    assert bit8_to_int(pc.read()) == 3


def test_add():
    ram = Ram256()
    pc = ProgramCounter()
    ir = InstructionRegister()
    registers = RegisterBank()
    ram.write(1, int_to_8bit(0), int_to_8bit(2))  # opcode
    ram.write(1, int_to_8bit(1), int_to_8bit(2))  # register 2
    ram.write(1, int_to_8bit(2), int_to_8bit(20))  # value 1


    ram.write(1, int_to_8bit(3), int_to_8bit(2))  # opcode
    ram.write(1, int_to_8bit(4), int_to_8bit(3))  # register 3
    ram.write(1, int_to_8bit(5), int_to_8bit(20))  # value 1


    ram.write(1, int_to_8bit(6), int_to_8bit(3))  # opcode add
    ram.write(1, int_to_8bit(7), int_to_8bit(2))  # register 2
    ram.write(1, int_to_8bit(8), int_to_8bit(3))  # register 3

    run(ram,pc, ir, registers,3)


    assert bit8_to_int(registers.read((0, 1))) == 40
    assert bit8_to_int(registers.read((1, 1))) == 20
    assert bit8_to_int(pc.read()) == 9
