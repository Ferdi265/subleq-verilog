`include "defines.vh"

module io_input(
    input clk,
    input areset,

    output reg eof,
    input in_read,
    output [`WORD_SIZE - 1 : 0] io_in
);
    reg [7 : 0] byte;
    integer fd;
    integer ret;

    task read;
        begin
            ret = $fread(byte, fd);
            eof = $feof(fd);
        end
    endtask

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
        read;
    end

    always @(posedge clk) if (in_read) read;

    assign io_in = byte;
endmodule
