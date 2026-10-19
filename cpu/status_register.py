from Hardware.bit_types import Bit
from Hardware.storage import SRLatch, update_sr_latch


class StatusRegister:
    def __init__(self):
        self.carry = SRLatch()
        self.zero = SRLatch()

    def update(self, load: Bit, carry: Bit, zero: Bit) -> None:
        update_sr_latch(self.carry, load, carry)
        update_sr_latch(self.zero, load, zero)

    def read_carry(self) -> Bit:
        return self.carry.read()

    def read_zero(self) -> Bit:
        return self.zero.read()