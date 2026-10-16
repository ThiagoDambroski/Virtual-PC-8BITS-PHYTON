from typing import cast

from Hardware.bit_types import Bit, Bits8
from Hardware.gates import nand, not_gate


class SRLatch:
    def __init__(self):
        self.q: Bit = cast(Bit, 0)
        self.q_bar: Bit = cast(Bit, 1)

    def update(self, set_n: Bit, reset_n: Bit) -> None:
        if set_n == 0 and reset_n == 0:
            raise ValueError("Invalid SR latch state")

        while True:
            old_q = self.q
            old_q_bar = self.q_bar

            self.q = nand(set_n, cast(Bit,self.q_bar))
            self.q_bar = nand(reset_n, self.q)

            if self.q == old_q and self.q_bar == old_q_bar:
                break


def update_sr_latch(latch: SRLatch, load: Bit, data: Bit) -> None:
    set_n = nand(load, data)
    reset_n = nand(not_gate(data), load)
    latch.update(set_n, reset_n)


class Register8:
    def __init__(self):
        self.latches = [SRLatch() for _ in range(8)]

    def update(self, load: Bit, data: Bits8) -> None:
        for i in range(8):
            update_sr_latch(self.latches[i], load, data[i])

    def read(self) -> Bits8:
        out_list: list[Bit] = []

        for latch in self.latches:
            out_list.append(cast(Bit,latch.q))

        return cast(Bits8, tuple(out_list))
