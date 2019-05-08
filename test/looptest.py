import test_v
from test_hl import *

class LoopTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(inrange = (0, 16), iterations = 20, preserve = ["_ZERO", "_ONE", "N15", "in"], **kwargs)

    def expected(self):
        return [1]

test = """
main:
    JEQ in N15 rone
    MOV i N15
loop:
    SUB i _ONE
    JEQ in i rone
    JMP loop

rzero:
    MOV out _ZERO
    HLT
rone:
    MOV out _ONE
    HLT

i: 0

N15: 15

_ZERO: 0
_ONE: 1
_TEMP0: NONE
_TEMP1: NONE
_TEMP2: NONE

@0xff00
in: NONE

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    LoopTester(program = test, iterations = 20).run()
