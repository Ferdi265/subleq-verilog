import test_v
from test_hl import *
from random import randrange

class BitTester(LabelPreservingTester, InputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(inaddr = 0xff21, outaddr = 0xff20, preserve = ["_ZERO", "_ONE", "N15", "in0", "in1"], **kwargs)
        self.pretests = [
            self.test_abcd_ff00,
            self.test_abcd_00ff
        ]
    
    def test_abcd_ff00(self):
        return [
            0xabcd, 0xff00
        ]

    def test_abcd_00ff(self):
        return [
            0xabcd, 0x00ff
        ]

    def get_input(self):
        return [
            randrange(0, 0x10000),
            randrange(0, 0x10000),
        ]

    def expected(self):
        return [self.input[0] ^ self.input[1]]

test = """
main:
    MOV bxa_a in0
    MOV bxa_b in1
    JAL sub_retaddr bitwise_xor
    MOV out bxr_xor
    HLT

sub_power: NONE
sub_i: NONE
sub_retaddr: NONE
bxa_a: NONE
bxa_b: NONE
bxr_xor: NONE
bitwise_xor:
    CLEAR bxr_xor
    JGEZ bxa_a bx_skip_a15
        SUB bxa_a POWERS15
        JGEZ bxa_b bx_xor15
            SUB bxa_b POWERS15
            JMP bx_skip15
bx_skip_a15:
    JGEZ bxa_b bx_skip15
        SUB bxa_b POWERS15
bx_xor15:
        ADD bxr_xor POWERS15
bx_skip15:
    MOV sub_i N15
bx_loop:
    JLEZ sub_i bx_ret
    SUB sub_i N1

    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    JLT bxa_a sub_power bx_skip_apow
        SUB bxa_a sub_power
        JLT bxa_b sub_power bx_xorpow
            SUB bxa_b sub_power
            JMP bx_loop
bx_skip_apow:
    JLT bxa_b sub_power bx_loop
        SUB bxa_b sub_power
bx_xorpow:
        ADD bxr_xor sub_power
        JMP bx_loop
bx_ret:
    JR sub_retaddr

N15: 15

POWERS: _ONE

_ZERO: 0
N1:
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

@0xff20 
out: NONE
in0: NONE
in1: NONE
@0xffff _HALT:

"""

if __name__ == "__main__":
    BitTester(program = test, iterations = 20).run()
