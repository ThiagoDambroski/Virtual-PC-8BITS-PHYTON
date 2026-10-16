from typing import cast

from Hardware.bit_types import Bit, Bits2, Bits3, Bits5, Bits6, Bits7, Bits8
from Hardware.gates import and_gate, dmux4way_gate, mux4way8bit_gate, mux_gate8bit, not_gate
from Hardware.storage import Register8


def registers_select(a: Register8, b: Register8, sel: Bit) -> Bits8:
    return mux_gate8bit(sel, a.read(), b.read())


def load_between_address(
    register_a: Register8,
    register_b: Register8,
    load: Bit,
    address: Bit,
    data: Bits8,
) -> None:
    load_a = and_gate(load, not_gate(address))
    load_b = and_gate(load, address)
    register_a.update(load_a, data)
    register_b.update(load_b, data)


def read_between_address(
    register_a: Register8,
    register_b: Register8,
    address: Bit,
) -> Bits8:
    return mux_gate8bit(address, register_a.read(), register_b.read())


class Ram2:
    def __init__(self):
        self.register_a = Register8()
        self.register_b = Register8()

    def write(self, load: Bit, address: Bit, data: Bits8) -> None:
        load_between_address(self.register_a, self.register_b, load, address, data)

    def read(self, address: Bit) -> Bits8:
        return read_between_address(self.register_a, self.register_b, address)


def write_between_ram2(
    ram_a: Ram2,
    ram_b: Ram2,
    load: Bit,
    address_bits: Bits2,
    data: Bits8,
) -> None:
    load_a = and_gate(load, not_gate(address_bits[1]))
    load_b = and_gate(load, address_bits[1])
    ram_a.write(load_a, address_bits[0], data)
    ram_b.write(load_b, address_bits[0], data)


def read_between_ram2(ram_a: Ram2, ram_b: Ram2, address_bits: Bits2) -> Bits8:
    return mux_gate8bit(
        address_bits[1],
        ram_a.read(address_bits[0]),
        ram_b.read(address_bits[0]),
    )


class Ram4:
    def __init__(self):
        self.ram_a = Ram2()
        self.ram_b = Ram2()

    def write(self, load: Bit, address_bits: Bits2, data: Bits8) -> None:
        write_between_ram2(self.ram_a, self.ram_b, load, address_bits, data)

    def read(self, address_bits: Bits2) -> Bits8:
        return read_between_ram2(self.ram_a, self.ram_b, address_bits)


def write_between_ram4(
    ram_a: Ram4,
    ram_b: Ram4,
    load: Bit,
    address_bits: Bits3,
    data: Bits8,
) -> None:
    chosen_bit = address_bits[2]
    internal_bits = cast(Bits2, address_bits[:2])
    load_a = and_gate(load, not_gate(chosen_bit))
    load_b = and_gate(load, chosen_bit)
    ram_a.write(load_a, internal_bits, data)
    ram_b.write(load_b, internal_bits, data)


def read_between_ram4(ram_a: Ram4, ram_b: Ram4, address_bits: Bits3) -> Bits8:
    chosen_bit = address_bits[2]
    internal_bits = cast(Bits2, address_bits[:2])
    return mux_gate8bit(
        chosen_bit,
        ram_a.read(internal_bits),
        ram_b.read(internal_bits),
    )


class Ram8:
    def __init__(self):
        self.ram_a = Ram4()
        self.ram_b = Ram4()

    def write(self, load: Bit, address_bits: Bits3, data: Bits8) -> None:
        write_between_ram4(self.ram_a, self.ram_b, load, address_bits, data)

    def read(self, address_bits: Bits3) -> Bits8:
        return read_between_ram4(self.ram_a, self.ram_b, address_bits)


def write_between_4_ram8(
    ram_a: Ram8,
    ram_b: Ram8,
    ram_c: Ram8,
    ram_d: Ram8,
    load: Bit,
    address_bits: Bits5,
    data: Bits8,
) -> None:
    internal_address = cast(Bits3, address_bits[:3])
    bank_select = cast(Bits2, address_bits[3:5])
    load_a, load_b, load_c, load_d = dmux4way_gate(bank_select, load)
    ram_a.write(load_a, internal_address, data)
    ram_b.write(load_b, internal_address, data)
    ram_c.write(load_c, internal_address, data)
    ram_d.write(load_d, internal_address, data)


def read_between_4_ram8(
    ram_a: Ram8,
    ram_b: Ram8,
    ram_c: Ram8,
    ram_d: Ram8,
    address_bits: Bits5,
) -> Bits8:
    internal_address = cast(Bits3, address_bits[:3])
    bank_select = cast(Bits2, address_bits[3:5])
    return mux4way8bit_gate(
        bank_select,
        ram_a.read(internal_address),
        ram_b.read(internal_address),
        ram_c.read(internal_address),
        ram_d.read(internal_address),
    )


class Ram32:
    def __init__(self):
        self.ram_a = Ram8()
        self.ram_b = Ram8()
        self.ram_c = Ram8()
        self.ram_d = Ram8()

    def write(self, load: Bit, address_bits: Bits5, data: Bits8) -> None:
        write_between_4_ram8(
            self.ram_a,
            self.ram_b,
            self.ram_c,
            self.ram_d,
            load,
            address_bits,
            data,
        )

    def read(self, address_bits: Bits5) -> Bits8:
        return read_between_4_ram8(
            self.ram_a,
            self.ram_b,
            self.ram_c,
            self.ram_d,
            address_bits,
        )


def write_between_ram32(
    ram_a: Ram32,
    ram_b: Ram32,
    load: Bit,
    address_bits: Bits6,
    data: Bits8,
) -> None:
    chosen_bit = address_bits[5]
    internal_bits = cast(Bits5, address_bits[:5])
    load_a = and_gate(load, not_gate(chosen_bit))
    load_b = and_gate(load, chosen_bit)
    ram_a.write(load_a, internal_bits, data)
    ram_b.write(load_b, internal_bits, data)


def read_between_ram32(ram_a: Ram32, ram_b: Ram32, address_bits: Bits6) -> Bits8:
    chosen_bit = address_bits[5]
    internal_bits = cast(Bits5, address_bits[:5])
    return mux_gate8bit(
        chosen_bit,
        ram_a.read(internal_bits),
        ram_b.read(internal_bits),
    )


class Ram64:
    def __init__(self):
        self.ram_a = Ram32()
        self.ram_b = Ram32()

    def write(self, load: Bit, address_bits: Bits6, data: Bits8) -> None:
        write_between_ram32(self.ram_a, self.ram_b, load, address_bits, data)

    def read(self, address_bits: Bits6) -> Bits8:
        return read_between_ram32(self.ram_a, self.ram_b, address_bits)


def write_between_ram64(
    ram_a: Ram64,
    ram_b: Ram64,
    load: Bit,
    address_bits: Bits7,
    data: Bits8,
) -> None:
    chosen_bit = address_bits[6]
    internal_bits = cast(Bits6, address_bits[:6])
    load_a = and_gate(load, not_gate(chosen_bit))
    load_b = and_gate(load, chosen_bit)
    ram_a.write(load_a, internal_bits, data)
    ram_b.write(load_b, internal_bits, data)


def read_between_ram64(ram_a: Ram64, ram_b: Ram64, address_bits: Bits7) -> Bits8:
    chosen_bit = address_bits[6]
    internal_bits = cast(Bits6, address_bits[:6])
    return mux_gate8bit(
        chosen_bit,
        ram_a.read(internal_bits),
        ram_b.read(internal_bits),
    )


class Ram128:
    def __init__(self):
        self.ram_a = Ram64()
        self.ram_b = Ram64()

    def write(self, load: Bit, address_bits: Bits7, data: Bits8) -> None:
        write_between_ram64(self.ram_a, self.ram_b, load, address_bits, data)

    def read(self, address_bits: Bits7) -> Bits8:
        return read_between_ram64(self.ram_a, self.ram_b, address_bits)


def write_between_ram128(
    ram_a: Ram128,
    ram_b: Ram128,
    load: Bit,
    address_bits: Bits8,
    data: Bits8,
) -> None:
    chosen_bit = address_bits[7]
    internal_bits = cast(Bits7, address_bits[:7])
    load_a = and_gate(load, not_gate(chosen_bit))
    load_b = and_gate(load, chosen_bit)
    ram_a.write(load_a, internal_bits, data)
    ram_b.write(load_b, internal_bits, data)


def read_between_ram128(
    ram_a: Ram128,
    ram_b: Ram128,
    address_bits: Bits8,
) -> Bits8:
    chosen_bit = address_bits[7]
    internal_bits = cast(Bits7, address_bits[:7])
    return mux_gate8bit(
        chosen_bit,
        ram_a.read(internal_bits),
        ram_b.read(internal_bits),
    )


class Ram256:
    def __init__(self):
        self.ram_a = Ram128()
        self.ram_b = Ram128()

    def write(self, load: Bit, address_bits: Bits8, data: Bits8) -> None:
        write_between_ram128(self.ram_a, self.ram_b, load, address_bits, data)

    def read(self, address_bits: Bits8) -> Bits8:
        return read_between_ram128(self.ram_a, self.ram_b, address_bits)
