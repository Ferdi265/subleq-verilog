import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/asm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/asm_test/')

from hlsim import *
import test_hl

from subprocess import check_output

class VSimAssembler(SimAssembler):
    def simulate(self, n = None):
        with open("/tmp/memory.hex", "w") as f:
            for i in range(0x10000):
                f.write("{:04x}\n".format(self.get_addr(i)))
        with open("/tmp/stdin.txt", "w") as f:
            pass

        dump = check_output([os.path.dirname(os.path.realpath(__file__)) + "/../subleq", "+autotest"], cwd = os.path.dirname(os.path.realpath(__file__)) + "/../").decode()
        i = 0
        for line in dump.split("\n")[:-1]:
            addr, entries = line.split(": ")
            for j, entry in enumerate(entries.split(" ")):
                self.set_addr(i + j, int(entry, 16))
            i += 16

        sys.stdout.write(".")
        sys.stdout.flush()

test_hl.Asm = create_assembler([HlAssembler, VSimAssembler, StringInputAssembler, Assembler])
