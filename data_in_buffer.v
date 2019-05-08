`include "defines.vh"

module data_in_buffer(
    input clk,
    input areset,

    input [`WORD_SIZE - 1 : 0] data_in,
    output [`WORD_SIZE - 1 : 0] data_in_0,
    output [`WORD_SIZE - 1 : 0] data_in_1,
    output [`WORD_SIZE - 1 : 0] data_in_2
);
    wire clk;
    wire areset;

    wire [`WORD_SIZE - 1 : 0] data_in;
    wire [`WORD_SIZE - 1 : 0] data_in_0;
    wire [`WORD_SIZE - 1 : 0] data_in_1;
    wire [`WORD_SIZE - 1 : 0] data_in_2;

    reg [`WORD_SIZE - 1 : 0] data_buf_1;
    reg [`WORD_SIZE - 1 : 0] data_buf_2;

    always @(posedge clk) begin
        data_buf_2 <= data_buf_1;
        data_buf_1 <= data_in;
    end

    always @(areset) if (areset) begin
        data_buf_2 = 0;
        data_buf_1 = 0;
    end

    assign data_in_0 = data_in;
    assign data_in_1 = data_buf_1;
    assign data_in_2 = data_buf_2;
endmodule
