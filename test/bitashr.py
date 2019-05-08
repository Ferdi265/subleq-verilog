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
        return [neg2twos(twos2neg(self.input[0]) >> self.input[1])]

test = """
main:
    MOV bra_a in0
    MOV bra_b in1
    JAL sub_retaddr bitwise_ashr
    MOV out brr_ashr
    HLT

sub_power: NONE
sub_i: NONE
sub_retaddr: NONE
bra_a: NONE
bra_b: NONE
brr_ashr: NONE
brv_j: NONE
brv_topbit: NONE
bitwise_ashr:
    CLEAR brr_ashr
    JEQZ bra_b br_reta
    JLT bra_b _ZERO br_fixarg
    JGE bra_b N16 br_fixarg
    JMP br_afterfix
br_fixarg:
    MOV bra_b N16
br_afterfix:

    JGEZ bra_a br_skiptop
        SUB bra_a POWERS15
        MOV brv_topbit N1
        JMP br_aftertop
br_skiptop:
    MOV brv_topbit _ZERO
br_aftertop:

    MOV sub_i N16
    MOV brv_j N16
    SUB brv_j bra_b

    JLEZ brv_topbit br_skip_toploop
br_toploop:
    JLE sub_i brv_j br_skip_toploop
    SUB sub_i N1

    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    ADD brr_ashr sub_power
    JMP br_toploop
br_skip_toploop:

    MOV sub_i N15
    SUB brv_j N1

    JLEZ brv_topbit br_skiptop2
        MOV sub_power POWERS
        ADD sub_power brv_j
        LDI sub_power sub_power
        
        ADD brr_ashr sub_power
br_skiptop2:

br_loop:
    JLEZ brv_j br_ret
    SUB sub_i N1
    SUB brv_j N1

    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    JLT bra_a sub_power br_loop
    SUB bra_a sub_power

    MOV sub_power POWERS
    ADD sub_power brv_j
    LDI sub_power sub_power

    ADD brr_ashr sub_power
    JMP br_loop

br_reta:
    MOV brr_ashr bra_a
br_ret:
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
