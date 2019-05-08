from test_toy import *
from random import randrange

def gentests(n):
    for i in range(n):
        print(">> test {}".format(i))
        reg1, reg2, reg3 = genregs()

        data1 = randrange(0, 256)
        data2 = randrange(0, 16)

        regs = [0] * 16
        regs[reg1] = data1
        regs[reg2] = data2
        regs[reg3] = (data1 >> data2) & (2**16 - 1)
        print("-- running with R{:01X} = {:04x}, R{:01X} = {:04x} => R{:01X}".format(reg1, data1, reg2, data2, reg3))
        run([], [
            toy_inst(7, reg1, data1),
            toy_inst(7, reg2, data2),
            toy_inst(6, reg3, reg1, reg2),
            0x0000
        ], regs)

if __name__ == "__main__":
    gentests(20)
