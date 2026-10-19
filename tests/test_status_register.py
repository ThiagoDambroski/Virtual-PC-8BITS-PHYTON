from cpu.status_register import StatusRegister


def test_status_register_initial_values():
    status = StatusRegister()

    assert status.read_carry() == 0
    assert status.read_zero() == 0


def test_status_register_sets_flags():
    status = StatusRegister()

    status.update(1, 1, 1)

    assert status.read_carry() == 1
    assert status.read_zero() == 1


def test_status_register_clears_flags():
    status = StatusRegister()

    status.update(1, 1, 1)
    status.update(1, 0, 0)

    assert status.read_carry() == 0
    assert status.read_zero() == 0


def test_status_register_holds_when_load_is_zero():
    status = StatusRegister()

    status.update(1, 1, 0)
    status.update(0, 0, 1)

    assert status.read_carry() == 1
    assert status.read_zero() == 0