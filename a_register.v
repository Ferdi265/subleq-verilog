`include "defines.vh"

module a_register(
    input clk,
    input areset,

    input set,
    input [`WORD_SIZE - 1 : 0] in,
    output [`WORD_SIZE - 1 : 0] out
);
    reg [`WORD_SIZE - 1 : 0] a;

    always @(posedge clk) if (set) a <= in;
    always @(areset) if (areset) a <= 0;

    assign out = a;
endmodule
