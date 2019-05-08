`define WORD_SIZE 16

`define STATE_BITS 3
`define FETCH_A   3'b000
`define DEREF_A   3'b001
`define FETCH_B   3'b010
`define DEREF_B   3'b011
`define STORE_SUB 3'b100
`define FETCH_C   3'b101
`define HALT      3'b110

`define INTERACTIVE ($test$plusargs("i") || $test$plusargs("interactive"))
