import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import test_v
from test_hl import *

class ToyProgramTester(LabelPreservingTester, InputTester, ExpectedOutputTester):
    def __init__(self, memory = [], registers = [], **kwargs):
        super().__init__(iterations = 1, inaddr = 0xfe00, outaddr = 0xff10, preserve = ["_ZERO", "_ONE"], **kwargs)
        self.memory = memory
        self.registers = registers

    def get_input(self):
        return self.memory

    def check_message(self):
        super().check_message()
        print("!! status: [", end = "")
        first = True
        for a in range(0xff00, 0xff08):
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{:04x}".format(self.asm.get_addr(a)), end = "")
        print("]")

    def expected(self):
        return self.registers

    def run(self):
        if not self.run_tests():
            sys.exit(1)

test = """
main:
    MOV toy_status N1
    MOV R0 _ZERO
    MOV toy_pc N16
main_loop:
    MOV toy_status N2
    MOV toy_addr TOY_MEMORY
    ADD toy_addr toy_pc
    LDI dca_inst toy_addr

    ADD toy_pc N1

    MOV toy_status N3
    JAL sub_retaddr decode

    MOV toy_status N4
    MOV toy_addr TOY_MEMORY
    MOV toy_ra0 TOY_REGISTERS
    MOV toy_ra1 TOY_REGISTERS
    MOV toy_ra2 TOY_REGISTERS
    ADD toy_ra0 dcr_imm0
    ADD toy_ra1 dcr_imm1
    ADD toy_ra2 dcr_imm2
    ADD toy_addr dcr_addr

    MOV branch_target branch_table
    ADD branch_target dcr_opc
    LDI branch_target branch_target

    JR branch_target
branch_target: NONE
branch_table: branch_table_start
branch_table_start:
    toy_hlt
    toy_add
    toy_sub
    toy_and
    toy_xor
    toy_shl
    toy_ashr
    toy_lda
    toy_ld
    toy_st
    toy_ldi
    toy_sti
    toy_bz
    toy_bp
    toy_jr
    toy_jl
toy_hlt:
    HLT
toy_add:
    LDI toy_ra1 toy_ra1
    LDI toy_ra2 toy_ra2
    ADD toy_ra1 toy_ra2
    STI toy_ra1 toy_ra0
    JMP main_loop
toy_sub:
    LDI toy_ra1 toy_ra1
    LDI toy_ra2 toy_ra2
    SUB toy_ra1 toy_ra2
    STI toy_ra1 toy_ra0
    JMP main_loop
toy_and:
    LDI baa_a toy_ra1
    LDI baa_b toy_ra2
    JAL sub_retaddr bitwise_and
    STI bar_and toy_ra0
    JMP main_loop
toy_xor:
    LDI bxa_a toy_ra1
    LDI bxa_b toy_ra2
    JAL sub_retaddr bitwise_xor
    STI bxr_xor toy_ra0
    JMP main_loop
toy_shl:
    LDI bla_a toy_ra1
    LDI bla_b toy_ra2
    JAL sub_retaddr bitwise_shl
    STI blr_shl toy_ra0
    JMP main_loop
toy_ashr:
    LDI bra_a toy_ra1
    LDI bra_b toy_ra2
    JAL sub_retaddr bitwise_ashr
    STI brr_ashr toy_ra0
    JMP main_loop
toy_lda:
    STI dcr_addr toy_ra0
    JMP main_loop
toy_ld:
    LDI toy_addr toy_addr
    STI toy_addr toy_ra0
    JMP main_loop
toy_st:
    LDI toy_ra0 toy_ra0
    STI toy_ra0 toy_addr
    JMP main_loop
toy_ldi:
    LDI baa_a toy_ra2
    MOV baa_b MASK_TOYADDR
    JAL sub_retaddr bitwise_and
    LDI toy_ra0 bar_and
    JMP main_loop
toy_sti:
    LDI baa_a toy_ra2
    MOV baa_b MASK_TOYADDR
    JAL sub_retaddr bitwise_and
    STI toy_ra0 bar_and
    JMP main_loop
toy_bz:
    LDI toy_ra0 toy_ra0
    JEQZ toy_ra0 branch_safe
    JMP main_loop
toy_bp:
    LDI toy_ra0 toy_ra0
    JGT toy_ra0 _ZERO branch_safe
    JMP main_loop
branch_safe:
    MOV toy_pc dcr_addr
    JMP main_loop
toy_jr:
    LDI baa_a toy_ra0
    MOV baa_b MASK_TOYADDR
    JAL sub_retaddr bitwise_and
    MOV toy_pc bar_and
    JMP main_loop
toy_jl:
    STI toy_pc toy_ra0
    MOV toy_pc dcr_addr
    JMP main_loop

toy_ra0: NONE
toy_ra1: NONE
toy_ra2: NONE
toy_addr: NONE

sub_retaddr: NONE
sub_i: NONE
sub_power: NONE

decode:
    CLEAR dcr_opc
    CLEAR dcr_imm0
    CLEAR dcr_imm1
    JGEZ dca_inst dc_skip15
        SUB dca_inst POWERS15
        ADD dcr_opc N8
dc_skip15:
    MOV sub_i N15
dc_loop:
    SUB sub_i _ONE
    JLE sub_i N2 dc_ret

    JEQ sub_i N7 dc_addr
    JEQ sub_i N3 dc_imm2
    JMP dc_regular
dc_addr:
    MOV dcr_addr dca_inst
    JMP dc_regular
dc_imm2:
    MOV dcr_imm2 dca_inst
dc_regular:
    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    JLT dca_inst sub_power dc_loop
    SUB dca_inst sub_power

    MOV sub_power POWERS
    ADD sub_power sub_i

    JGE sub_i N12 dc_opcode
    JGE sub_i N8 dc_imm0
dc_imm1:
    SUB sub_power N4
    LDI sub_power sub_power
    ADD dcr_imm1 sub_power
    JMP dc_loop
dc_imm0:
    SUB sub_power N8
    LDI sub_power sub_power
    ADD dcr_imm0 sub_power
    JMP dc_loop
dc_opcode:
    SUB sub_power N12
    LDI sub_power sub_power
    ADD dcr_opc sub_power
    JMP dc_loop
dc_ret:
    JR sub_retaddr

baa_a: NONE
baa_b: NONE
bar_and: NONE
bitwise_and:
    CLEAR bar_and
    JGEZ baa_a ba_skip_a15
        SUB baa_a POWERS15
        JGEZ baa_b ba_skip15
            SUB baa_b POWERS15
            ADD bar_and POWERS15
            JMP ba_skip15
ba_skip_a15:
    JGEZ baa_b ba_skip15
    SUB baa_b POWERS15
ba_skip15:
    MOV sub_i N14
ba_loop:
    JLEZ sub_i ba_ret
    SUB sub_i N1
    
    MOV sub_power POWERS
    ADD sub_power sub_i
    LDI sub_power sub_power

    JLT baa_a sub_power ba_skip_apow
        SUB baa_a sub_power
        JLT baa_b sub_power ba_loop
            SUB baa_b sub_power
            ADD bar_and sub_power
            JMP ba_loop
ba_skip_apow:
    JLT baa_b sub_power ba_loop
        SUB baa_b sub_power
        JMP ba_loop
ba_ret:
    JR sub_retaddr

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

MASK_TOYADDR: 0xff

N3: 3
N5: 5
N6: 6
N7: 7
N9: 9
N10: 10
N11: 11
N12: 12
N13: 13
N14: 14
N15: 15

TOY_MEMORY: MEM0
TOY_REGISTERS: R0
POWERS: _ONE

_ZERO: N0:
    0
_ONE: N1:
    0x0001
N2: 0x0002
N4: 0x0004
N8: 0x0008
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

_TEMP0: NONE
_TEMP1: NONE
_TEMP2: NONE

@0xfe00
MEM0:

@0xff00
toy_pc: NONE
toy_status: NONE
dca_inst: NONE
dcr_opc: NONE
dcr_imm0: NONE
dcr_imm1: NONE
dcr_imm2: NONE
dcr_addr: NONE

@0xff10
R0:

@0xffff
_HALT: NONE
"""

def run(predatamem, progmem, regs):
    ToyProgramTester(
        program = test,
        memory = predatamem + [0] * (16 - len(predatamem)) + progmem,
        registers = regs + [0] * (16 - len(regs) - 1)
    ).run()

def toy_inst(opc, imm0, imm1, imm2 = None):
    if imm2 == None:
        data = imm1
    else:
        data = (imm1 << 4) + imm2
    return (opc << 12) + (imm0 << 8) + data

def genregs():
    reg1 = randrange(1, 16)

    reg2 = None
    while reg2 == None or reg2 == reg1:
        reg2 = randrange(1, 16)

    reg3 = None
    while reg3 == None or reg3 == reg1 or reg3 == reg2:
        reg3 = randrange(1, 16)

    return reg1, reg2, reg3
