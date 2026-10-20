from Hardware.bit_types import Bits8
from Hardware.storage import Register8


class InstructionRegister:

    def __init__(self):
        self.register8:Register8 = Register8()

    def load(self,data:Bits8) -> None:
        self.register8.update(1, data)
    def read(self) -> Bits8:
        return self.register8.read()
