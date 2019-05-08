import test_v
from test_hl import *

class JlezTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["_ZERO", "_ONE", "in"], **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pretests = [
            self.test_min,
            self.test_max
        ]

    def test_min(self):
        return [0x8000]

    def test_max(self):
        return [0x7fff]

    def expected(self):
        return [int(twos2neg(self.input[0]) <= 0)]

test = """
main:
    JLEZ in lez
    MOV out _ZERO
    HLT
lez:
    MOV out _ONE
    HLT

_ZERO: 0
_ONE: 1
_TEMP0: NONE

@0xff00
in:

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    JlezTester(program = test, iterations = 20).run()
