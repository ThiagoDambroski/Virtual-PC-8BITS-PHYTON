from logicGates import *

class SRLatch:
    def __init__(self):
        self.q = 0
        self.q_bar = 1
    def update(self,set_n,reset_n):
         if set_n == 0 and  reset_n == 0:
             raise ValueError('invalid')
         while True:
            old_q = self.q
            old_q_bar = self.q_bar
            self.q = nand(set_n,self.q_bar)
            self.q_bar = nand(reset_n,self.q)
            if self.q == old_q and self.q_bar == old_q_bar:
                break

def UISRLatch(inlatch:SRLatch,load,data):
    inlatch.update(nand(load,data),nand(not_gate(data),load))


class Register8:
    def __init__(self):
        self.latch_arr:list[SRLatch] = []
        for i in range(0,8):
            self.latch_arr.append(SRLatch())
    def update(self,load,data_arr:list):
        for i in range(0,8):
            UISRLatch(self.latch_arr[i],load,data_arr[i])

    def read(self):
        list_return_lsb = []
        for i in self.latch_arr:
            list_return_lsb.append(i.q)
        return list_return_lsb

def registers_select(a:Register8,b:Register8,sel:int):
    list_a = a.read()
    list_b = b.read()
    return_list = mux_gate8bit(sel,list_a,list_b)
    return return_list


def load_between_address(re1:Register8,re2:Register8, load: int, address: int,data_arr:list[int]):
    load_r1 = and_gate(load, not_gate(address))
    load_r2 = and_gate(load, address)
    re1.update(load_r1,data_arr)
    re2.update(load_r2,data_arr)

def read_between_address(re1:Register8,re2:Register8, address: int):
    return mux_gate8bit(address,re1.read(),re2.read())

class Ram2:
    def __init__(self):
        self.re1 = Register8()
        self.re2 = Register8()

    def write(self,load,address,data_arr:list):
        load_between_address(self.re1,self.re2,load,address,data_arr)
    def read(self,address):
        return read_between_address(self.re1,self.re2,address)



def write_between_ram2(ram_a:Ram2,ram_b:Ram2,load,address_bits:list[int],data):
    load_a = and_gate(load, not_gate(address_bits[1]))
    load_b = and_gate(load, address_bits[1])
    ram_a.write(load_a,address_bits[0],data)
    ram_b.write(load_b,address_bits[0],data)

def read_between_ram2(ram_a:Ram2,ram_b:Ram2,address_bits:list[int]):
    return mux_gate8bit(address_bits[1],ram_a.read(address_bits[0]),ram_b.read(address_bits[0]))

class Ram4:
    def __init__(self):
        self.a = Ram2()
        self.b = Ram2()
    def write(self,load,address_bits:list[int],data):
        write_between_ram2(self.a,self.b,load,address_bits,data)
    def read(self,address_bits:list[int]):
        return read_between_ram2(self.a,self.b,address_bits)



def write_between_ram4(ram_a:Ram4,ram_b:Ram4,load,address_bits:list[int],data):
    choosen_bit = address_bits[2]
    others_bits = address_bits[:2]
    load_a =  and_gate(not_gate(choosen_bit),load)
    load_b =  and_gate(choosen_bit,load)
    ram_a.write(load_a,others_bits,data)
    ram_b.write(load_b,others_bits,data)

def read_between_ram4(ram_a:Ram4,ram_b:Ram4,address_bits:list[int]):
    chossen_bit = address_bits[2]
    others_bit = address_bits[:2]
    return mux_gate8bit(chossen_bit,ram_a.read(others_bit),ram_b.read(others_bit))


class Ram8:
    def __init__(self):
        self.ram_a = Ram4()
        self.ram_b = Ram4()
    def write(self,load,address_bits:list[int],data):
        write_between_ram4(self.ram_a,self.ram_b,load,address_bits,data)
    def read(self,address_bits:list[int]):
        return read_between_ram4(self.ram_a,self.ram_b,address_bits)

def write_between_4_ram8(ram_a:Ram8,ram_b:Ram8,ram_c:Ram8,ram_d:Ram8,
                         load:int,address_bits:list[int],data:list[int]):
    internal_adress = address_bits[:3]
    bank_select = address_bits[3:5]
    load_a,load_b,load_c,load_d = dmux4way_gate(bank_select,load)
    ram_a.write(load_a,internal_adress,data)
    ram_b.write(load_b, internal_adress, data)
    ram_c.write(load_c, internal_adress, data)
    ram_d.write(load_d, internal_adress, data)

def load_between_4_ram8(ram_a:Ram8,ram_b:Ram8,ram_c:Ram8,ram_d:Ram8,address_bits:list[int]):
    internal_bits = address_bits[:3]
    bank_bits = address_bits[3:5]
    return mux4way8bit_gate(bank_bits,ram_a.read(internal_bits),ram_b.read(internal_bits),
                            ram_c.read(internal_bits),ram_d.read(internal_bits))

class Ram32:
    def __init__(self):
        self.ram_a = Ram8()
        self.ram_b = Ram8()
        self.ram_c = Ram8()
        self.ram_d = Ram8()
    def write(self,load:int,address_bit:list[int],data:list[int]):
        write_between_4_ram8(self.ram_a,self.ram_b,self.ram_c,self.ram_d,load,address_bit,data)
    def read(self,address_bit:list[int]):
        return load_between_4_ram8(self.ram_a,self.ram_b,self.ram_c,self.ram_d,address_bit)



#test latc
latch = SRLatch()
latch.update(0,1)

assert latch.q == 1
assert latch.q_bar == 0

latch.update(1,1)

assert latch.q == 1
assert latch.q_bar == 0

latch.update(1,0)

assert latch.q == 0
assert latch.q_bar == 1

latch.update(1,1)

assert latch.q == 0
assert latch.q_bar == 1

#teste registor 8
register = Register8()

assert len(register.latch_arr) == 8
assert register.latch_arr[0] is not register.latch_arr[1]

register = Register8()

register.update(1, [1, 0, 1, 0, 0, 0, 0, 0])

assert register.read() == [1, 0, 1, 0, 0, 0, 0, 0]

a = [1, 0, 1, 0, 0, 0, 0, 0]
b = [0, 1, 0, 1, 0, 0, 0, 0]

assert mux_gate8bit(0, a, b) == a
assert mux_gate8bit(1, a, b) == b


register = Register8()
register2 = Register8()
five_in_bit = int_to_8bit(5)
load_between_address(register,register2,1,0,five_in_bit)
assert register.read() == five_in_bit

#test ram
ram2 = Ram2()
ram2.write(1,0,int_to_8bit(5))
ram2.write(1,1,int_to_8bit(10))
print(bit8_to_int(ram2.read(0)))
print(bit8_to_int(ram2.read(1)))

#test ram4
ram4 = Ram4()
ram4.write(1,[0,0],int_to_8bit(10))


assert  ram4.read([0,0]) == int_to_8bit(10)


#test ram8
ram8 = Ram8()
ram8.write(1,[0,0,0],int_to_8bit(10))

assert ram8.read([0,0,0]) == int_to_8bit(10)

# teste Ram32

ram32 = Ram32()
ram32.write(1,[0,0,0,0,0],int_to_8bit(50))


assert ram32.read([0,0,0,0,0]) == int_to_8bit(50)
