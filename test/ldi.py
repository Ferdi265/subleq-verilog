from mov import CopyTester

lditest = """
main:
    LDI out inptr
    HLT

_TEMP0: NONE
inptr: in

@0xff00
in:

@0xff10
out:

@0xffff
_HALT:
"""

if __name__ == "__main__":
    CopyTester(program = lditest, iterations = 20).run()
