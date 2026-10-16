from Hardware.gates import dmux4way_gate, mux4way8bit_gate
from Hardware.storage import Register8
from Hardware.bit_types import Bits2,Bits8

class RegisterBank:
     def __init__(self):
         self.R0 = Register8()
         self.R1 = Register8()
         self.R2 = Register8()
         self.R3 = Register8()

     def write(self, address_bits: Bits2, data: Bits8) -> None:
          load_r0, load_r1, load_r2, load_r3 = dmux4way_gate(address_bits, 1)
          self.R0.update(load_r0, data)
          self.R1.update(load_r1, data)
          self.R2.update(load_r2, data)
          self.R3.update(load_r3, data)

     def read(self,address_bit:Bits2) -> Bits8:
          return mux4way8bit_gate(address_bit, self.R0.read(), self.R1.read(), self.R2.read(),self.R3.read())