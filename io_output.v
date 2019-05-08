`include "defines.vh"

module io_output(
    input clk,
    input areset,

    input out_write,
    input [`WORD_SIZE - 1 : 0] io_out
);
    wire clk;
    wire areset;

    wire out_write;
    wire [`WORD_SIZE - 1 : 0] io_out;
endmodule
