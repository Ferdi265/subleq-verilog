import test_v
from test_hl import *
from random import randrange

class BitTester(LabelPreservingTester, InputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(inaddr = 0xff21, outaddr = 0xff20, preserve = ["_ZERO", "_ONE", "N15", "number", "bit"], **kwargs)
        self.pretests = [
            self.test_min,
            self.test_neg
        ]

    def test_min(self):
        return [0x8000, 15]

    def test_neg(self):
        return [0x8001, 0]

    def get_input(self):
        return [
            randrange(0, 0x10000),
            randrange(0, 16)
        ]

    def expected(self):
        number = self.input[0]
        bit = self.input[1]
        return [int(number & 2**bit != 0)]

test = """
main:
    MOV bta_x number
    MOV bta_n bit
    JAL bta_retaddr bittest
    MOV out bta_ret
    HLT

bittest:
    JGEZ bta_x bt_skip15
        JEQ bta_n N15 bt_ret1
        SUB bta_x POWERS15
        JMP bt_start_loop
bt_skip15:
    JEQ bta_n N15 bt_ret0
bt_start_loop:
    MOV btv_i N15
bt_loop:
    JEQZ btv_i bt_ret0
    SUB btv_i _ONE
    MOV btv_power POWERS
    ADD btv_power btv_i
    LDI btv_power btv_power
    JLT bta_x btv_power bt_skip
        JEQ bta_n btv_i bt_ret1
        SUB bta_x btv_power
        JMP bt_loop
bt_skip:
    JEQ bta_n btv_i bt_ret0
    JMP bt_loop
bt_ret0:
    MOV bta_ret _ZERO
    JMP bt_ret
bt_ret1:
    MOV bta_ret _ONE
bt_ret:
    JR bta_retaddr

N15: 15

POWERS: _ONE

_ZERO: 0
_ONE:
    0x0001
    0x0002
    0x0004
    0x0008
    0x0010
    0x0020
    0x0040
    0x0080
    0x0100
    0x0200
    0x0400
    0x0800
    0x1000
    0x2000
    0x4000
POWERS15:
    0x8000

@0xff00
_TEMP0: NONE
_TEMP1: NONE
_TEMP2: NONE

@0xff10
bta_x: NONE
bta_n: NONE
bta_ret: NONE
bta_retaddr: NONE
btv_i: NONE
btv_power: NONE

@0xff20 
out: NONE
number: 0x8000
bit: 15
@0xffff _HALT:

"""

if __name__ == "__main__":
    BitTester(program = test, iterations = 20).run()
