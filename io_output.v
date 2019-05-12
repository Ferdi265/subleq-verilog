`include "defines.vh"

module io_output(
    input clk,
    input areset,

    output ack,
    input req,
    input [`WORD_SIZE - 1 : 0] data
);
    reg [`IO_STATE_BITS - 1 : 0] state;
    wire [`IO_STATE_BITS - 1 : 0] next_state;

    always @(posedge clk) state <= next_state;
    always @(areset) if (areset) state <= `IO_WAITREQ;

    assign next_state =
        state == `IO_WAITREQ && req ? `IO_DOWORK :
        state == `IO_DOWORK ? `IO_WAITACK :
        state == `IO_WAITACK && !req ? `IO_WAITREQ :
        state;

    assign ack = state == `IO_WAITACK;

    integer fd;

    initial begin
        if (`INTERACTIVE)
            fd = $fopen("/dev/stdout", "w");
        else
            fd = $fopen("output.txt", "w");

        if (fd == 0) begin
            $display("[ERROR] cannot write stdout");
            $finish;
        end
    end

    always @(posedge clk) if (state == `IO_DOWORK) begin
        $display("[IO OUT]: writing %h", data[7 : 0]);
        $fwrite(fd, "%s", data[7 : 0]);
    end
endmodule
