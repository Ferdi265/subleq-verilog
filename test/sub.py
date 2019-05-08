import test_v
from test_hl import *

class SubTester(LabelPreservingTester, TwoRandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["in0", "in1"], **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pretests = [
            self.test_min_one
        ]

    def test_min_one(self):
        return [0x8000, 1]

    def expected(self):
        return [neg2twos(twos2neg(self.input[0]) - twos2neg(self.input[1]))]

test = """
main:
    MOV out in0
    SUB out in1
    HLT

_TEMP0: NONE

@0xff00
in0: NONE
in1: NONE

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    SubTester(program = test, iterations = 20).run()
