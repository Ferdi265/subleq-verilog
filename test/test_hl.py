import sys
from random import randrange
from hlsubleq.sim import *
from hlsubleq.hlasm import *

Asm = create_assembler([HlAssembler, SimAssembler, StringInputAssembler, Assembler])

class Tester:
    def __init__(self, program, n = None, iterations = 1000, **kwargs):
        self.program = program
        self.n = n
        self.iterations = iterations
        self.pretests = []

    def get_input(self):
        pass

    def setup(self, input_fn):
        pass

    def check(self):
        return True

    def setup_message(self):
        pass

    def check_message(self):
        pass

    def run_test(self, input_fn):
        self.setup(input_fn)

        self.asm.simulate(self.n)

        if self.check():
            self.count += 1
        else:
            print("!! test failed")
            self.setup_message()
            self.check_message()
            self.passed = False

        return self.passed

    def execute(self):
        self.asm = Asm(
            instring = self.program
        )
        self.asm.assemble()

        self.passed = True
        self.count = 0

        for pretest_setup in self.pretests:
            if not self.run_test(pretest_setup):
                break

        if not self.passed:
            return

        for it in range(self.iterations):
            if not self.run_test(self.get_input):
                break

    def run_tests(self):
        print("Testing.. {} pretests and {} iterations".format(len(self.pretests), self.iterations))
        self.execute()
        print(".. {} tests passed".format(self.count))
        return self.passed

    def run(self):
        sys.exit(0 if self.run_tests() else 1)

class LabelPreservingTester(Tester):
    def __init__(self, preserve = [], **kwargs):
        super().__init__(**kwargs)
        self.preserve = preserve

    def setup(self, input_fn):
        super().setup(input_fn)
        self.values = {
            key: self.asm.get_addr(self.asm.program.labels[key]) for key in self.preserve
        }

    def setup_message(self):
        super().setup_message()
        print("!! to preserve: {", end = "")
        first = True
        for e in self.values.items():
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{}: {:04x}".format(
                e[0],
                e[1]
            ), end = "")
        print("}")

    def check(self):
        return (
            super().check() and
            all(map(
                lambda e: self.asm.get_addr(self.asm.program.labels[e[0]]) == e[1],
                self.values.items()
            ))
        )

    def check_message(self):
        super().check_message()
        print("!! actual values: {", end = "")
        first = True
        for e in self.values.items():
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{}: {:04x}".format(
                e[0],
                self.asm.get_addr(self.asm.program.labels[e[0]])
            ), end = "")
        print("}")

class InputTester(Tester):
    def __init__(self, inaddr = 0xff00, **kwargs):
        super().__init__(**kwargs)
        self.inaddr = inaddr

    def get_input(self):
        return []

    def setup(self, input_fn = None):
        if input_fn == None:
            input_fn = self.get_input
        self.input = input_fn()
        for i in range(len(self.input)):
            iaddr = self.inaddr + i
            idata = self.input[i] 
            self.asm.set_addr(iaddr, idata)

    def setup_message(self):
        print("!! input was: [", end = "")
        first = True
        for inp in self.input:
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{:04x}".format(inp), end = "")
        print("]")

class RandomInputTester(InputTester):
    def __init__(self, inrange = (0x0000, 0x10000), inlen = 1, **kwargs):
        super().__init__(**kwargs)
        self.inrange = inrange
        self.inlen = inlen

    def get_input(self):
        inp = []
        for i in range(self.inlen):
            iaddr = self.inaddr + i
            idata = randrange(self.inrange[0], self.inrange[1])
            inp.append(idata)
        return inp

class TwoRandomInputTester(RandomInputTester):
    def __init__(self, **kwargs):
        super().__init__(inlen = 2, **kwargs)

class ExpectedOutputTester(Tester):
    def __init__(self, outaddr = 0xff10, **kwargs):
        super().__init__(**kwargs)
        self.outaddr = outaddr

    def expected(self):
        return [1]

    def check(self):
        addr = self.outaddr
        for output in self.expected():
            if self.asm.get_addr(addr) != output:
                return False
            addr += 1
        return True

    def check_message(self):
        expected = self.expected()
        outlen = len(expected)
        print("!! output was: [", end = "")
        first = True
        for outaddr in range(self.outaddr, self.outaddr + outlen):
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{:04x}".format(self.asm.get_addr(outaddr)), end = "")
        print("]")
        print("!! expected: [", end = "")
        first = True
        for output in expected:
            if not first:
                print(", ", end = "")
            else:
                first = False
            print("{:04x}".format(output), end = "")
        print("]")
