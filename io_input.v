`include "defines.vh"

module io_input(
    input clk,
    input areset,

    output reg eof,
    output ack,
    input req,
    output [`WORD_SIZE - 1 : 0] data
);
    reg [7 : 0] byte;
    reg [`IO_STATE_BITS - 1 : 0] state;
    wire [`IO_STATE_BITS - 1 : 0] next_state;

    always @(posedge clk) state <= next_state;
    always @(areset) if (areset) begin
        state <= `IO_WAITREQ;
        eof <= 0;
    end

    assign next_state =
        state == `IO_WAITREQ && req ? `IO_DOWORK :
        state == `IO_DOWORK ? `IO_WAITACK :
        state == `IO_WAITACK && !req ? `IO_WAITREQ :
        state;

    assign ack = state == `IO_WAITACK;

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

    always @(posedge clk) if (state == `IO_DOWORK) begin
        ret = $fread(byte, fd);
        eof = $feof(fd);
        $display("[IO IN]: reading %h, eof = %h", data[7 : 0], eof);
    end

    assign data = byte;
endmodule
