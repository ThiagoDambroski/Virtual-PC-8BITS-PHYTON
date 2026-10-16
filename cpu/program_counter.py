from Hardware.arithmetic import increment_8bit
from Hardware.bit_types import Bits8
from Hardware.storage import Register8


class ProgramCounter:
    def __init__(self):
        self.current_address = Register8()

    def read(self) -> Bits8:
        return self.current_address.read()

    def increment(self) -> None:
        new_address, _ = increment_8bit(self.current_address.read())
        self.current_address.update(1, new_address)
