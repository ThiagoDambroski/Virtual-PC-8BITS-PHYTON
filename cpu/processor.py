from Hardware.bit_types import Bits8
from Hardware.memory import Ram256
from cpu.program_counter import ProgramCounter


def fetch(ram: Ram256, pc: ProgramCounter) -> Bits8:
    current_pc = pc.read()
    fetched_value = ram.read(current_pc)
    pc.increment()
    return fetched_value
