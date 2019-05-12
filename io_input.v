`include "defines.vh"

module io_input(
    output reg eof,
    output reg ack,
    input req,
    output [`WORD_SIZE - 1 : 0] data
);
    reg [7 : 0] byte;
    integer fd;
    integer ret;

    initial begin
        eof = 0;
        ack = 0;
        if (`INTERACTIVE)
            fd = $fopen("/dev/stdin", "r");
        else
            fd = $fopen("input.txt", "r");

        if (fd == 0) begin
            $display("[ERROR] cannot read stdin");
            $finish;
        end

        while (1) begin
            wait (req);
            ret = $fread(byte, fd);
            eof = $feof(fd);
            ack = 1;
            wait (!req);
            ack = 0;
        end
    end

    assign data = byte;
endmodule
