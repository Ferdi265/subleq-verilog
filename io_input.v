`include "defines.vh"

module io_input(
    input clk,
    input areset,

    output eof,
    input in_read,
    output [`WORD_SIZE - 1 : 0] io_in
);
    wire clk;
    wire areset;

    reg eof;
    wire in_read;
    wire [`WORD_SIZE - 1 : 0] io_in;

    reg [7 : 0] byte;
    integer fd;
    integer ret;

    initial begin
        eof = 0;
        if (`INTERACTIVE)
            fd = $fopen("/dev/stdin", "r");
        else
            fd = $fopen("input.txt", "r");

        if (fd == 0) begin
            $display("[ERROR] cannot read stdin");
            $finish;
        end
    end

    always @(posedge clk) if (in_read) begin
        ret = $fread(byte, fd);
        eof = $feof(fd);
    end

    assign io_in = byte;
endmodule