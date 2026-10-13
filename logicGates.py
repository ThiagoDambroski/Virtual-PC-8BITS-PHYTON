from typing import Literal, cast

Bit = Literal[0,1]

Bits8 = tuple[Bit,Bit,Bit,Bit,Bit,Bit,Bit,Bit]

def nand(a:Bit,b:Bit) -> Bit:
    return 0 if a and b else 1

def not_gate (a:Bit) -> Bit:

    return nand(a,a)

def and_gate(a:Bit, b:Bit) -> Bit:
    return not_gate(nand(a, b))

def or_gate(a:Bit, b:Bit) -> Bit:

    return nand(not_gate(a), not_gate(b))

def xor_gate(a:Bit,b:Bit) -> Bit:
    return and_gate(or_gate(a, b), (nand(a, b)))

def mux_gate(a:Bit,b:Bit,sel:Bit) -> Bit:
    not_sel = not_gate(sel)
    first_gate = and_gate(a,not_sel)
    second_gate = and_gate(b,sel)
    return or_gate(first_gate,second_gate)

def mux_gate8bit(sel: Bit, a: Bits8, b: Bits8) -> Bits8:
    out_list: list[Bit] = []

    for i in range(8):
        out_list.append(mux_gate(a[i], b[i], sel))

    return cast(Bits8, tuple(out_list))


def dmux_gate(sel:Bit,load:Bit) -> tuple[Bit,Bit]:
    return_a = and_gate(not_gate(sel),load)
    return_b = and_gate(sel,load)
    return return_a,return_b

def dmux4way_gate(sel:list[Bit],load:Bit) -> tuple[Bit,Bit,Bit,Bit]:
    active_first,active_second = dmux_gate(sel[1],load)

    return_a,return_b =  dmux_gate(sel[0],active_first)
    return_c,return_d = dmux_gate(sel[0],active_second)
    return return_a,return_b,return_c,return_d

def mux4way8bit_gate(sel:list[Bit],a:list[Bit],b:list[Bit],c:list[Bit],d:list[Bit]) -> Bits8:
    first = mux_gate8bit(sel[0],a,b)
    second = mux_gate8bit(sel[0],c,d)
    return mux_gate8bit(sel[1],first,second)

#converter
def int_to_8bit(a:int) -> list[Bit]:
    out_list:list[Bit] = []
    for i in range(8):
        bit: Bit = 1 if ((a >> i) & 1) else 0
        out_list.append(bit)
    return out_list

def bit8_to_int(bits8: list[Bit]) -> int:
    tot = 0

    for i in range(8):
        tot |= bits8[i] << i

    return tot

#Add

def half_adder_gate(a:Bit,b:Bit):
    sum_bit = xor_gate(a,b)
    carry = and_gate(a,b)
    return sum_bit,carry

def full_adder_gate(a:Bit,b:Bit,carry_in:Bit):
    sum_bit_p,c= half_adder_gate(a,b)
    sum_bit_t,d= half_adder_gate(sum_bit_p,carry_in)
    carry_out = or_gate(c,d)
    return sum_bit_t,carry_out

def add_8bit_gate(a: list[Bit], b: list[Bit]) -> tuple[list[Bit], Bit]:
    out_list: list[Bit] = []

    sum_bit, internal_carry = half_adder_gate(a[0], b[0])
    out_list.append(sum_bit)

    for i in range(1, 8):
        sum_bit, internal_carry = full_adder_gate(a[i],b[i],internal_carry)
        out_list.append(sum_bit)

    return out_list, internal_carry

def add_from_int(a: int, b: int):
    sum8bits,carryout = add_8bit_gate(int_to_8bit(a), int_to_8bit(b))

    return bit8_to_int(sum8bits),carryout

#test

x = int_to_8bit(15)
y = int_to_8bit(10)
tot,carry = add_8bit_gate(x,y)



