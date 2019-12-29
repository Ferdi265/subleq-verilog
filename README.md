# subleq-verilog

A Verilog implementation of the
[SUBLEQ](https://en.wikipedia.org/wiki/One_instruction_set_computer#Subtract_and_branch_if_less_than_or_equal_to_zero)
machine, including a test suite using
[hl-subleq-tools](https://github.com/Ferdi265/hl-subleq-tools).

## SUBLEQ

The SUBLEQ instruction is a combined arithmetic and conditional jump
instruction:

```
subleq a, b, c
```

also sometimes written

```
subleq [a], [b], c
```

It is equivalent to the following C-like pseudo code:

```c
*b -= *a;
if (*b <= 0) pc = c;
```

This single instruction is sufficient to implement arbitrary programs.

### Implementation

The CPU in this repository implements a variant of
SUBLEQ using Two's Complement arithmetic with word-addressed memory and
configurable word-size. (default is 16 bits)

Each SUBLEQ instruction is 3 consecutive possibly unaligned memory words.
Execution starts at address `0`.

Any fetch from the highest address (`0xffff` in the 16-bit variant) halts the
machine. This includes operand fetches / deref.

### Extensions

This implementation includes two additional memory-mapped devices not (yet)
included in the [hl-subleq-tools](https://github.com/Ferdi265/hl-subleq-tools)
simulator:

Any write to the second-highest address (`0xfffe` in the 16-bit variant) writes
to stdout.

Any read from the third-highest address (`0xfffd` in the 16-bit variant) reads
from stdin.

## Verilog Implementation

The Verilog implementation is intended to be used with the
[Icarus Verilog](http://iverilog.icarus.com/) simulator, available in most
package managers as `iverilog`.

The test bench will read a few files from disk on startup:

- the memory image will be loaded as hex from `memory.hex`
- the stdin mmio device will read from `input.txt` (or `/dev/stdin` if
  interactive mode is on)
- the stdout mmio device will write to `output.txt` (or `/dev/stdout` if
  interactive mode is on)

The test bench accepts a few options via "plusargs":

- `+i` or `+interactive`: enable interactive mode
- `+autotest`: dump whole memory image on halt, useful for automated tests
- `+debug`: print internal debug information every cycle, including a dump of
  the first 128 words of memory (edit `test_subleq.v` to change the dump window)

Run `make` to build the test bench and run `./subleq [+options...]` to run the
simulator on the test bench.

## Test Suite

The [test/](test/) subdirectory contains a test suite for the Verilog
implementation, testing various HLSUBLEQ programs using random test vectors
(inspired by [QuickCheck](https://hackage.haskell.org/package/QuickCheck)).

The [test/toytests/](test/toytests) subdirectory contains further test cases
testing a software emulator of the
[TOY CPU architecure](https://introcs.cs.princeton.edu/java/62toy/)
written in HLSUBLEQ. This is currently the most complicated program written in
HLSUBLEQ.

Both directories contain a `run_tests.sh` script that runs every test case in
the directory.
