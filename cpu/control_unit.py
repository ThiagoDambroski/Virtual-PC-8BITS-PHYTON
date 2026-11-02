from Hardware.alu import alu_result
from Hardware.memory import Ram256
from cpu.halt_register import HaltRegister
from cpu.processor import fetch
from cpu.program_counter import ProgramCounter
from cpu.registers import RegisterBank
from cpu.register_decoder import decode_register


def execute_load_immediate(ram: Ram256, pc: ProgramCounter,register_bank:RegisterBank) -> None:
    register = fetch(ram,pc)
    value = fetch(ram,pc)
    address = decode_register(register)
    register_bank.write(address,value)

def execute_add(ram: Ram256, pc: ProgramCounter,register_bank:RegisterBank) -> None:
    destination = fetch(ram,pc)
    source = fetch(ram,pc)
    destination_decoded = decode_register(destination)
    source_decoded = decode_register(source)

    result,carry,zero = alu_result(register_bank.read(destination_decoded),
                                   register_bank.read(source_decoded),(0,0))#add

    register_bank.write(destination_decoded,result)

def execute_halt(halt_register:HaltRegister):
    halt_register.halt()