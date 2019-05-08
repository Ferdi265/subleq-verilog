import test_v
from test_hl import *

class JgezTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["_ZERO", "_ONE", "in"], **kwargs)

    def expected(self):
        return [int(twos2neg(self.input[0]) >= 0)]

test = """
main:
    JGEZ in gez
    MOV out _ZERO
    HLT
gez:
    MOV out _ONE
    HLT

_ZERO: 0
_ONE: 1
_TEMP0: NONE
_TEMP1: NONE

@0xff00
in:

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    JgezTester(program = test, iterations = 20).run()
