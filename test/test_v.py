import sys
import os.path
from subprocess import check_output
from hlsubleq.sim import *
from hlsubleq.hlasm import *

import test_hl

subleq_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")

class VSimAssembler(SimAssembler):
    def simulate(self, n = None):
        with open(subleq_dir + "/memory.hex", "w") as f:
            for i in range(0x10000):
                f.write("{:04x}\n".format(self.get_addr(i)))

        dump = check_output([subleq_dir + "/subleq", "+autotest"], cwd = subleq_dir).decode()
        i = 0
        for line in dump.split("\n")[:-1]:
            if "$finish" in line:
                continue

            addr, entries = line.split(": ")
            for j, entry in enumerate(entries.split(" ")):
                self.set_addr(i + j, int(entry, 16))
            i += 16

        sys.stdout.write(".")
        sys.stdout.flush()

test_hl.Asm = create_assembler([HlAssembler, VSimAssembler, StringInputAssembler, Assembler])
