from Hardware.bit_types import Bits2,Bits8

def decode_register(a:Bits8) -> Bits2:
    for i in range(2,8):
        if a[i] == 1:
            raise ValueError("Invalid Register")
    return a[0],a[1]