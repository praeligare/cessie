import sys
import random
import cocotb
from cocotb.triggers import Timer

class TB:
    andmod = 0x0
    ormod = 0x1
    add = 0x2
    sub = 0x6
    slt = 0x7
    nor = 0xC
    dut = cocotb.top

    def __init__(self, mode = add, cycle=2):
        TB.dut.sel.value = mode

    def randomize_input(self):
        TB.dut.a.value = int.from_bytes(random.randbytes(4), sys.byteorder)
        TB.dut.b.value = int.from_bytes(random.randbytes(4), sys.byteorder)

@cocotb.test(skip=False)
async def and_with_zero(dut):
    tb = TB(TB.andmod)

    tb.randomize_input()
    dut.a.value = 0x0000_0000

    await Timer(10, units='ns')
    assert dut.s.value == 0x0000_0000, f'AND mismatch: s: {dut.s.value} != {dut.a.value}.'

@cocotb.test(skip=False)
async def and_with_maximum(dut):
    tb = TB(TB.andmod)

    tb.randomize_input()
    dut.a.value = 0xFFFF_FFFF

    await Timer(10, units='ns')
    assert dut.s.value == dut.b.value, f'AND mismatch: s: output != {dut.b.value}.'

@cocotb.test(skip=False)
async def and_by_one(dut):
    tb = TB(TB.andmod)

    for i in range(10):
        tb.randomize_input()
        dut.a.value = i

        await Timer(10, units='ns')
        assert dut.s.value == dut.a.value & dut.b.value, f'AND mismatch: s: {dut.s.value} != {dut.a.value & dut.b.value}.'

@cocotb.test(skip=False)
async def and_by_n_times(dut):
    tb = TB(TB.andmod)

    for i in range(10):
        tb.randomize_input()

        await Timer(10, units='ns')
        assert dut.s.value == (dut.a.value & dut.b.value) & 0xFFFF_FFFF, f'AND mismatch: s: {hex(dut.s.value.integer & 0xFFFF_FFFF)} != {hex((dut.a.value.integer & dut.b.value.integer) & 0xFFFF_FFFF)}.'

##############################################################

@cocotb.test(skip=False)
async def or_with_zero(dut):
    tb = TB(TB.ormod)

    tb.randomize_input()
    dut.a.value = 0x0000_0000

    await Timer(10, units='ns')
    assert dut.s.value == dut.b.value, f'OR mismatch: s: {dut.s.value} != {dut.b.value}.'

@cocotb.test(skip=False)
async def or_with_maximum(dut):
    tb = TB(TB.ormod)

    tb.randomize_input()
    dut.a.value = 0xFFFF_FFFF

    await Timer(10, units='ns')
    assert dut.s.value == 0xFFFF_FFFF, f'OR mismatch: s: {dut.s.value} != {dut.a.value}.'

@cocotb.test(skip=False)
async def or_by_one(dut):
    tb = TB(TB.ormod)
    dut.a.value = 0x0000_0000
    await Timer(1, units='ns')

    for i in range(10):
        a = dut.a.value
        tb.randomize_input()
        dut.a.value = a + 1

        await Timer(10, units='ns')
        a_or_b = (bin(dut.a.value | dut.b.value)[2:]).zfill(32)
        assert str(dut.s.value) == str(a_or_b), f'OR mismatch: s: {dut.s.value} != {a_or_b}.'

@cocotb.test(skip=False)
async def or_by_n_times(dut):
    tb = TB(TB.ormod)

    for i in range(10):
        tb.randomize_input()

        await Timer(10, units='ns')
        a_or_b = (bin(dut.a.value | dut.b.value)[2:]).zfill(32)
        assert str(dut.s.value) == str(a_or_b), f'OR mismatch: s: {dut.s.value} != {a_or_b}.'


##############################################################

@cocotb.test(skip=False)
async def add_with_zero(dut):
    tb = TB(TB.add)

    for i in range(10):
        tb.randomize_input()
        dut.a.value = 0

        await Timer(10, units='ns')
        assert dut.s.value == dut.b.value, f'Adding mismatch: s: {dut.s.value} != {dut.b.value}.'


@cocotb.test(skip=False)
async def add_by_one(dut):
    tb = TB(TB.add)

    for i in range(10):
        tb.randomize_input()
        dut.a.value = 1

        await Timer(10, units='ns')
        assert dut.s.value == dut.b.value + 1, f'Adding mismatch: s: {dut.s.value} != {dut.b.value + 1}.'


@cocotb.test(skip=False)
async def add_by_maximum(dut):
    tb = TB(TB.add)

    dut.a.value = 0xFFFF_FFFF
    dut.b.value = 0xFFFF_FFFF
   
    await Timer(10, units='ns')
    assert dut.s.value == (dut.a.value + dut.b.value) & 0xFFFF_FFFF, f'Adding mismatch: s: {hex(dut.s.value.integer)} != {hex((dut.a.value.integer + dut.b.value.integer) & 0xFFFF_FFFF)}.'


@cocotb.test(skip=False)
async def add_by_n_times(dut):
    tb = TB(TB.add)

    for i in range(10):
        tb.randomize_input()

        await Timer(10, units='ns')
        assert dut.s.value == (dut.a.value + dut.b.value) & 0xFFFF_FFFF, f'Adding mismatch: s: {hex(dut.s.value.integer & 0xFFFF_FFFF)} != {hex((dut.a.value.integer + dut.b.value.integer) & 0xFFFF_FFFF)}.'

###############################################################

@cocotb.test(skip=False)
async def sub_with_zero(dut):
    tb = TB(TB.sub)

    for i in range(10):
        tb.randomize_input()
        dut.a.value = 0

        await Timer(10, units='ns')
        # Python uses int as 64 bits. We are representing it with only 32,
        # masking is needed when comparing negative numbers
        assert dut.s.value == -dut.b.value & 0xFFFF_FFFF, f'Subtracting mismatch: s: {hex(dut.s.value.integer)} != {hex(-dut.b.value.integer & 0xffff_ffff)}.'


@cocotb.test(skip=False)
async def sub_one_less_number(dut):
    tb = TB(TB.sub)

    for i in range(10):
        tb.randomize_input()
        dut.a.value = 1

        await Timer(10, units='ns')
        # Python uses int as 64 bits. We are representing it with only 32,
        # masking is needing when comparing negative numbers
        assert dut.s.value == (1-dut.b.value) & 0xFFFF_FFFF, f'Subtracting mismatch: s: {hex(dut.s.value.integer)} != {hex((1-dut.b.value.integer) & 0xffff_ffff)}.'


@cocotb.test(skip=False)
async def sub_by_maximum(dut):
    tb = TB(TB.sub)

    dut.a.value = 0xFFFF_FFFF
    dut.b.value = 0xFFFF_FFFF
   
    await Timer(10, units='ns')
    assert dut.s.value == (dut.a.value - dut.b.value) & 0xFFFF_FFFF, f'Subtracting mismatch: s: {hex(dut.s.value.integer)} != {hex((dut.a.value.integer - dut.b.value.integer) & 0xFFFF_FFFF)}.'


@cocotb.test(skip=False)
async def sub_by_n_times(dut):
    tb = TB(TB.sub)

    for i in range(10):
        tb.randomize_input()

        await Timer(10, units='ns')
        assert dut.s.value == (dut.a.value - dut.b.value) & 0xFFFF_FFFF, f'Adding mismatch: s: {hex(dut.s.value.integer & 0xFFFF_FFFF)} != {hex((dut.a.value.integer - dut.b.value.integer) & 0xFFFF_FFFF)}.'

###############################################################

@cocotb.test(skip=False)
async def slt_zero(dut):
    tb = TB(TB.slt)

    tb.randomize_input()
    dut.b.value = 0x0000_0000

    await Timer(10, units='ns')
    if int(dut.a.value) < int(dut.b.value):   
        assert dut.s.value == 0x0000_0001, f'SLT mismatch: s: {dut.s.value} != 1.'
    else:
        assert dut.s.value ==  0x0000_0000, f'SLT mismatch: s: {dut.s.value} != 0.'

@cocotb.test(skip=False)
async def slt_maximum(dut):
    tb = TB(TB.slt)

    tb.randomize_input()
    dut.a.value = 0xFFFF_FFFF

    await Timer(10, units='ns')
    if int(dut.a.value) > int(dut.b.value):   
        assert dut.s.value == 0x0000_0000, f'SLT mismatch: s: {dut.s.value} != 0.'
    else:
        assert dut.s.value ==  0x0000_0001, f'SLT mismatch: s: {dut.s.value} != 1.'

###############################################################

@cocotb.test(skip=False)
async def check_zero(dut):
    tb = TB(TB.andmod)

    tb.randomize_input()
    dut.b.value = 0x0000_0000

    await Timer(10, units='ns')
    assert dut.s.value ==  0x0, f'Flag mismatch: ZERO: {dut.s.value} != 00000000.'