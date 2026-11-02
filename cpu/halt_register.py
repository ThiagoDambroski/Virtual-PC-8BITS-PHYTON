from typing import cast

from Hardware.bit_types import Bit

class HaltRegister:
    def __init__(self):
        self.value:Bit  = cast(Bit,0)

    def read(self) -> Bit :
        return cast(Bit,self.value)
    def halt(self) -> None:
        self.value = 1
    def reset(self) -> None:
        self.value = 0