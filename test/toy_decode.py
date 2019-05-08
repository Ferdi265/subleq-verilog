import test_v
from test_hl import *
from random import randrange

class ToyDecodeTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(iterations = 1000, preserve = ["_ZERO", "_ONE", "N15", "inst"], **kwargs)

    def expected(self):
        inst = self.input[0]
        opc = (inst & 0xf000) >> 12
        imm0 = (inst & 0x0f00) >> 8
        imm1 = (inst & 0x00f0) >> 4
        imm2 = inst & 0x000f
        addr = inst & 0x00ff
        return [opc, imm0, imm1, imm2, addr]

test = """
main:
    MOV dca_inst inst
    JAL dca_retaddr decode
    MOV opc dcr_opc
    MOV imm0 dcr_imm0
    MOV imm1 dcr_imm1
    MOV imm2 dcr_imm2
    MOV addr dcr_addr
    HLT

dca_inst: NONE
dca_retaddr: NONE
dcr_opc: NONE
dcr_imm0: NONE
dcr_imm1: NONE
dcr_imm2: NONE
dcr_addr: NONE
dcv_i: NONE
dcv_power: NONE
decode:
    CLEAR dcr_opc
    CLEAR dcr_imm0
    CLEAR dcr_imm1
    JGEZ dca_inst dc_skip15
        SUB dca_inst POWERS15
        ADD dcr_opc N8
dc_skip15:
    MOV dcv_i N15
dc_loop:
    SUB dcv_i _ONE
    JLE dcv_i N2 dc_ret

    JEQ dcv_i N7 dc_addr
    JEQ dcv_i N3 dc_imm2
    JMP dc_regular
dc_addr:
    MOV dcr_addr dca_inst
    JMP dc_regular
dc_imm2:
    MOV dcr_imm2 dca_inst
dc_regular:
    MOV dcv_power POWERS
    ADD dcv_power dcv_i
    LDI dcv_power dcv_power

    JLT dca_inst dcv_power dc_loop
    SUB dca_inst dcv_power

    MOV dcv_power POWERS
    ADD dcv_power dcv_i

    JGE dcv_i N12 dc_opcode
    JGE dcv_i N8 dc_imm0
dc_imm1:
    SUB dcv_power N4
    LDI dcv_power dcv_power
    ADD dcr_imm1 dcv_power
    JMP dc_loop
dc_imm0:
    SUB dcv_power N8
    LDI dcv_power dcv_power
    ADD dcr_imm0 dcv_power
    JMP dc_loop
dc_opcode:
    SUB dcv_power N12
    LDI dcv_power dcv_power
    ADD dcr_opc dcv_power
    JMP dc_loop
dc_ret:
    JR dca_retaddr

N3: 3
N7: 7
N12: 12
N15: 15

POWERS: _ONE

_ZERO: 0
_ONE:
    0x0001
N2:  0x0002
N4: 0x0004
N8: 0x0008
N16: 0x0010
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

_TEMP0: NONE
_TEMP1: NONE
_TEMP2: NONE

@0xff00
inst: NONE

@0xff10
opc: NONE
imm0: NONE
imm1: NONE
imm2: NONE
addr: NONE

@0xffff
_HALT: NONE
"""

if __name__ == "__main__":
    ToyDecodeTester(program = test, iterations = 20).run()
