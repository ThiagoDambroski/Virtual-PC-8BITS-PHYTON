from Hardware.memory import Ram256
from cpu.processor import fetch
from cpu.program_counter import ProgramCounter
from cpu.registers import RegisterBank
from cpu.register_decoder import decode_register


def execute_load_immediate(ram: Ram256, pc: ProgramCounter,register_bank:RegisterBank) -> None:
    register = fetch(ram,pc)
    value = fetch(ram,pc)
    address = decode_register(register)
    register_bank.write(address,value)
    