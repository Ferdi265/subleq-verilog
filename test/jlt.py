import test_v
from test_hl import *

class JltTester(LabelPreservingTester, TwoRandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["_ZERO", "_ONE", "in0", "in1"], **kwargs)

    def expected(self):
        return [int(twos2neg(self.input[0]) < twos2neg(self.input[1]))]

test = """
main:
    JLT in0 in1 le
    MOV out _ZERO
    HLT
le:
    MOV out _ONE
    HLT

_ZERO: 0
_ONE: 1
_TEMP0: NONE
_TEMP1: NONE
_TEMP2: NONE

@0xff00
in0: NONE
in1: NONE

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    JltTester(program = test, iterations = 20).run()
