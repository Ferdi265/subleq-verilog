from mov import CopyTester

lditest = """
main:
    STI in outptr
    HLT

_TEMP0: NONE
outptr: out

@0xff00
in:

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    CopyTester(program = lditest, iterations = 20).run()
