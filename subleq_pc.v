`include "defines.vh"

module subleq_pc(
    input clk,
    input areset,

    input branch,
    input inc,
    input [`WORD_SIZE - 1 : 0] addr,
    output [`WORD_SIZE - 1 : 0] pc_out
);
    wire clk;
    wire areset;

    wire branch;
    wire inc;
    wire [`WORD_SIZE - 1 : 0] addr;
    wire [`WORD_SIZE - 1 : 0] pc_out;

    reg [`WORD_SIZE - 1 : 0] pc;

    always @(clk) begin
        if (branch) pc <= addr;
        else pc <= pc + inc;
    end

    always @(areset) if (areset) pc = 0;

    assign pc_out = pc;
endmodule
