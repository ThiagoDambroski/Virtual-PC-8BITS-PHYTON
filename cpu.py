import logicGates
import ram

registers = [0] * 4
pc = 0
carry = 0
zeroFlag = 0


def read_register(register_id):
    if not isinstance(register_id,int) or register_id< 0 or register_id> len(registers)-1:
        raise ValueError("Invalid register id")
    return registers[register_id]

def write_register(register_id, value):
    if not isinstance(register_id, int) or register_id < 0 or register_id > len(registers)-1:
        raise ValueError("Invalid register id")
    if not isinstance(value,int) or 0 > value or value > 0xff:
        raise ValueError("Invalid value")
    registers[register_id] = value


def fetch():
    global pc
    value = ram.read(pc)
    pc += 1
    if pc == 0x100:
        pc = 0
    return value

def step():
    global carry
    global zeroFlag
    opcode = fetch()
    if opcode == 0x02:
        registerId = fetch()
        value = fetch()
        write_register(registerId,value)
    elif opcode == 0x03:

        destination = fetch()
        source1 = fetch()
        source2 = fetch()

        value1 = read_register(source1)
        value2 = read_register(source2)

        value,carry,zeroFlag = addition(value1,value2)

        write_register(destination,value)

    else:
        raise ValueError("Invalid opcode")


def addition(input1,input2):
    value, icarry = logicGates.add_from_int(input1,input2)
    zero = int(value== 0)
    return value,icarry,zero


ram.write(0,0x02)
ram.write(1,0x02)
ram.write(2,10)#42
step()
print(read_register(0x02))
print(pc)

ram.write(3,0x02)
ram.write(4,0x01)
ram.write(5,100)
step()

ram.write(6,0x03)
ram.write(7,0x03)
ram.write(8,0x01)
ram.write(9,0x02)
step()

print(read_register(0x03))