import test_v
from test_hl import *

class CopyTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(preserve = ["in"], **kwargs)

    def expected(self):
        return [self.input[0]]

class MovTester(CopyTester):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pretests = [
            self.test_min
        ]

    def test_min(self):
        return [0x8000]


test = """
main:
    MOV out in
    HLT

_TEMP0: NONE

@0xff00
in:

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    MovTester(program = test, iterations = 20).run()
