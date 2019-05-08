import test_v
from test_hl import *

class JeqmTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["_ZERO", "_ONE", "in"], **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pretests = [
            self.test_min,
            self.test_minplusone,
            self.test_max,
            self.test_maxminusone,
            self.test_zero
        ]

    def test_min(self):
        return [0x8000]

    def test_minplusone(self):
        return [0x8001]
    
    def test_max(self):
        return [0x7fff]

    def test_maxminusone(self):
        return [0x7ffe]

    def test_zero(self):
        return [0]

    def expected(self):
        return [int(self.input[0] == 0x8000)]

test = """
main:
    JEQM in min
    MOV out _ZERO
    HLT
min:
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
    JeqmTester(program = test, iterations = 20).run()
