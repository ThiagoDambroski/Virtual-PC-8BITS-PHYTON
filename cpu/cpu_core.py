
from Hardware.gates import not_gate
from Hardware.memory import Ram256
from cpu.control_unit import execute_load_immediate, execute_add, execute_halt
from cpu.halt_register import HaltRegister
from cpu.instruction_decoder import decode_instruction
from cpu.instruction_register import InstructionRegister
from cpu.processor import fetch_opcode
from cpu.program_counter import ProgramCounter
from cpu.registers import RegisterBank


def step(ram:Ram256,pc:ProgramCounter,ir:InstructionRegister,
         registers:RegisterBank,halt_register:HaltRegister) -> None:
    fetch_opcode(ram,pc,ir)

    is_load,is_add,is_halt = decode_instruction(ir.read())
    if is_load:
        execute_load_immediate(ram,pc,registers)
    elif is_add:
        execute_add(ram,pc,registers)
    elif is_halt:
        execute_halt(halt_register)
    else:
        raise ValueError("Unknown instruction")



def run(ram:Ram256,pc:ProgramCounter,ir:InstructionRegister,
        registers:RegisterBank,halt_register:HaltRegister) -> None:

    while not_gate(halt_register.read()):
        step(ram,pc,ir,registers,halt_register)