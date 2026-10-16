import pytest

from Hardware.arithmetic import int_to_8bit
from Hardware.storage import Register8, SRLatch


def test_sr_latch_set_hold_reset():
    latch = SRLatch()

    latch.update(0, 1)
    assert latch.q == 1
    assert latch.q_bar == 0

    latch.update(1, 1)
    assert latch.q == 1
    assert latch.q_bar == 0

    latch.update(1, 0)
    assert latch.q == 0
    assert latch.q_bar == 1

    latch.update(1, 1)
    assert latch.q == 0
    assert latch.q_bar == 1


def test_sr_latch_rejects_invalid_input():
    latch = SRLatch()

    with pytest.raises(ValueError):
        latch.update(0, 0)


def test_register8_contains_independent_latches():
    register = Register8()
    assert len(register.latches) == 8
    assert register.latches[0] is not register.latches[1]


def test_register8_load_and_hold():
    register = Register8()
    first = int_to_8bit(5)
    second = int_to_8bit(10)

    register.update(1, first)
    assert register.read() == first

    register.update(0, second)
    assert register.read() == first
