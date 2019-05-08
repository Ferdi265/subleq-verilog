`include "defines.vh"

module memory(
    input clk,
    input areset,

    input load,
    input store,
    output [`WORD_SIZE - 1 : 0] mem_out,
    input [`WORD_SIZE - 1 : 0] mem_in,
    input [`WORD_SIZE - 1 : 0] addr
);
    wire clk;
    wire areset;

    wire load;
    wire store;
    wire [`WORD_SIZE - 1 : 0] mem_out;
    wire [`WORD_SIZE - 1 : 0] mem_in;
    wire [`WORD_SIZE - 1 : 0] addr;

    reg [`WORD_SIZE - 1 : 0] buffer[(1 << `WORD_SIZE) - 1 : 0];

    always @(clk) if (store) buffer[addr] <= mem_in;

    integer i;
    always @(areset) if (areset) begin
        for (i = 0; i < (1 << `WORD_SIZE); i = i + 1)
            buffer[i] = 0;
        $readmemh("memory.hex", buffer, 0, (1 << `WORD_SIZE) - 1);
    end

    assign mem_out = load ? buffer[addr] : 0;
endmodule
