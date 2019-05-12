`define WORD_SIZE 16

`define STATE_BITS 4
`define FETCH_A    4'b0000
`define WAIT_A     4'b0001
`define FINISH_A   4'b0010
`define DEREF_A    4'b0011
`define WAIT_DA    4'b0100
`define FETCH_B    4'b0101
`define WAIT_B     4'b0110
`define FINISH_B   4'b0111
`define DEREF_B    4'b1000
`define WAIT_DB    4'b1001
`define STORE_SUB  4'b1010
`define WAIT_STORE 4'b1011
`define FETCH_C    4'b1100
`define WAIT_C     4'b1101
`define HALT       4'b1111

`define INTERACTIVE ($test$plusargs("i") || $test$plusargs("interactive"))
