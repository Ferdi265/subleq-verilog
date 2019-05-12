`include "defines.vh"

module subleq_pc(
    input clk,
    input areset,

    input branch,
    input inc,
    input [`WORD_SIZE - 1 : 0] addr,
    output [`WORD_SIZE - 1 : 0] pc_out
);
    reg [`WORD_SIZE - 1 : 0] pc;

    always @(posedge clk) begin
        if (branch) pc <= addr;
        else pc <= pc + inc;
    end

    always @(areset) if (areset) begin
        pc <= 0;
    end

    assign pc_out = pc;
endmodule
