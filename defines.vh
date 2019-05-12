`define WORD_SIZE 16

`define STATE_BITS 4

`define FETCH_A    0
`define WAIT_A     1
`define DEREF_A    2
`define WAIT_DA    3
`define FETCH_B    4
`define WAIT_B     5
`define DEREF_B    6
`define WAIT_DB    7
`define STORE_SUB  8
`define WAIT_STORE 9
`define FETCH_C    10
`define WAIT_C     11
`define BRANCH     12
`define HALT       13

`define IO_STATE_BITS 2

`define IO_WAITREQ 0
`define IO_DOWORK  1
`define IO_WAITACK 2

`define INTERACTIVE ($test$plusargs("i") || $test$plusargs("interactive"))
