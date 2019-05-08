import test_v
from test_hl import *

class PtrTester(LabelPreservingTester, RandomInputTester, ExpectedOutputTester):
    def __init__(self, **kwargs):
        super().__init__(inrange = (0, 16), preserve = ["_ZERO", "_ONE", "POWERS", "in"], **kwargs)

    def expected(self):
        return [2**self.input[0]]

test = """
main:
    MOV out in
    ADD out POWERS
    LDI out out
    HLT

POWERS: _ONE

_ZERO: 0
_ONE:
    0x0001
    0x0002
    0x0004
    0x0008
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
    0x8000

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
    PtrTester(program = test, iterations = 20).run()
