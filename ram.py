
ram = [0] * 256

def read(addr):
    if isinstance(addr,int) and 0 <= addr < len(ram) :
        return ram[addr]
    raise ValueError("Invalid address")

def write(addr,value):

    if isinstance(addr,int) and isinstance(value,int) and 0 <= value < 256 and 0 <= addr < len(ram) :
       ram[addr] = value
       return

    raise ValueError("Invalid address or value")

#test
assert read(0) == 0
write(10,12)
assert read(10) == 12

try:
    read(-1)
except ValueError:
    print("OK")
else:
    raise ValueError("Somethins is wrong")


