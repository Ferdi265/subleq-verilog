import test_v
from test_hl import *
from random import randrange

class BitTester(LabelPreservingTester, InputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(inaddr = 0xff21, outaddr = 0xff20, preserve = ["_ZERO", "_ONE", "N15", "in0", "in1"], **kwargs)
        self.pretests = [
            self.test_abcd_4,
            self.test_f00f_7,
            self.test_abcd_15,
            self.test_4b00_2,
            self.test_beef_0,
            self.test_c0de_20,
            self.test_cafe_beef
        ]
    
    def test_abcd_4(self):
        return [
            0xabcd, 4
        ]
    
    def test_f00f_7(self):
        return [
            0xf00f, 7
        ]

    def test_abcd_15(self):
        return [
            0xabcd, 15
        ]

    def test_4b00_2(self):
        return [
            0x4b00, 2
        ]
            
    def test_beef_0(self):
        return [
            0xbeef, 0
        ]
    
    def test_c0de_20(self):
        return [
            0xc0de, 20
        ]

    def test_cafe_beef(self):
        return [
            0xcafe, 0xbeef
        ]

    def get_input(self):
        return [
            randrange(0, 0x10000),
            randrange(0, 0x10),
        ]

    def expected(self):
        return [(self.input[0] << self.input[1]) & (2**16 - 1)]

test = """
main:
    MOV bla_a in0
    MOV bla_b in1
    JAL sub_retaddr bitwise_shl
    MOV out blr_shl
    HLT

sub_power: NONE
sub_i: NONE
sub_retaddr: NONE
bla_a: NONE
bla_b: NONE
blr_shl: NONE
blv_j: NONE
bitwise_shl:
    CLEAR blr_shl
    JEQZ bla_b bl_reta
    JLT bla_b _ZERO bl_ret
    JGE bla_b N16 bl_ret

    MOV sub_i N16
    SUB sub_i bla_b
    MOV blv_j N16

bl_toploop:
    JLE blv_j sub_i bl_toploop_after
    SUB blv_j N1

    MOV sub_power POWERS
    ADD sub_power blv_j
    LDI sub_power sub_power

    JEQ blv_j N15 bl_toploop15
    JLT bla_a sub_power bl_toploop
bl_toploop_sub:
    SUB bla_a sub_power
    JMP bl_toploop
bl_toploop15:
    JGEZ bla_a bl_toploop
    JMP bl_toploop_sub
bl_toploop_after:

    MOV blv_j N16
bl_loop:
    JLEZ sub_i bl_ret
    SUB sub_i N1
    SUB blv_j N1

    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    JLT bla_a sub_power bl_loop
    SUB bla_a sub_power

    MOV sub_power POWERS
    ADD sub_power blv_j
    LDI sub_power sub_power

    ADD blr_shl sub_power
    JMP bl_loop

bl_reta:
    MOV blr_shl bla_a
bl_ret:
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
N16:
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
