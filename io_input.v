`include "defines.vh"

module io_input(
    input clk,
    input areset,

    output in_avail,
    input in_read,
    output [`WORD_SIZE - 1 : 0] io_in
);
    wire clk;
    wire areset;

    wire in_avail;
    wire in_read;
    wire [`WORD_SIZE - 1 : 0] io_in;

    assign in_avail = 0;
    assign io_in = 0;
endmodule
