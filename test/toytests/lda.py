from test_toy import *
from random import randrange

def gentests(n):
    for i in range(n):
        print(">> test {}".format(i))
        reg = randrange(1, 16)

        data = randrange(0, 256)

        regs = [0] * 16
        regs[reg] = data
        print("-- running with R{:01X} = {:04x}".format(reg, data))
        run([], [
            toy_inst(7, reg, data),
            0x0000
        ], regs)

if __name__ == "__main__":
    gentests(20)
