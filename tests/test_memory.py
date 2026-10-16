from Hardware.arithmetic import int_to_8bit
from Hardware.memory import Ram2, Ram4, Ram8, Ram32, Ram64, Ram128, Ram256


def test_ram2_addresses_are_independent():
    ram = Ram2()
    ram.write(1, 0, int_to_8bit(5))
    ram.write(1, 1, int_to_8bit(10))
    assert ram.read(0) == int_to_8bit(5)
    assert ram.read(1) == int_to_8bit(10)


def test_ram4_boundaries():
    ram = Ram4()
    ram.write(1, (0, 0), int_to_8bit(10))
    ram.write(1, (1, 1), int_to_8bit(40))
    assert ram.read((0, 0)) == int_to_8bit(10)
    assert ram.read((1, 1)) == int_to_8bit(40)


def test_ram8_boundaries():
    ram = Ram8()
    ram.write(1, (0, 0, 0), int_to_8bit(10))
    ram.write(1, (1, 1, 1), int_to_8bit(80))
    assert ram.read((0, 0, 0)) == int_to_8bit(10)
    assert ram.read((1, 1, 1)) == int_to_8bit(80)


def test_ram32_bank_boundaries():
    ram = Ram32()
    ram.write(1, (1, 1, 1, 0, 0), int_to_8bit(7))
    ram.write(1, (0, 0, 0, 1, 0), int_to_8bit(8))
    ram.write(1, (1, 1, 1, 1, 1), int_to_8bit(31))
    assert ram.read((1, 1, 1, 0, 0)) == int_to_8bit(7)
    assert ram.read((0, 0, 0, 1, 0)) == int_to_8bit(8)
    assert ram.read((1, 1, 1, 1, 1)) == int_to_8bit(31)


def test_ram64_boundary_between_banks():
    ram = Ram64()
    ram.write(1, (1, 1, 1, 1, 1, 0), int_to_8bit(31))
    ram.write(1, (0, 0, 0, 0, 0, 1), int_to_8bit(32))
    assert ram.read((1, 1, 1, 1, 1, 0)) == int_to_8bit(31)
    assert ram.read((0, 0, 0, 0, 0, 1)) == int_to_8bit(32)


def test_ram128_boundary_between_banks():
    ram = Ram128()
    ram.write(1, (1, 1, 1, 1, 1, 1, 0), int_to_8bit(63))
    ram.write(1, (0, 0, 0, 0, 0, 0, 1), int_to_8bit(64))
    assert ram.read((1, 1, 1, 1, 1, 1, 0)) == int_to_8bit(63)
    assert ram.read((0, 0, 0, 0, 0, 0, 1)) == int_to_8bit(64)


def test_ram256_boundaries_and_hold():
    ram = Ram256()
    address_0 = int_to_8bit(0)
    address_127 = int_to_8bit(127)
    address_128 = int_to_8bit(128)
    address_255 = int_to_8bit(255)

    ram.write(1, address_0, int_to_8bit(10))
    ram.write(1, address_127, int_to_8bit(20))
    ram.write(1, address_128, int_to_8bit(30))
    ram.write(1, address_255, int_to_8bit(40))

    assert ram.read(address_0) == int_to_8bit(10)
    assert ram.read(address_127) == int_to_8bit(20)
    assert ram.read(address_128) == int_to_8bit(30)
    assert ram.read(address_255) == int_to_8bit(40)

    ram.write(0, address_255, int_to_8bit(99))
    assert ram.read(address_255) == int_to_8bit(40)
