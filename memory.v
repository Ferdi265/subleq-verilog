`include "defines.vh"

module memory(
    input clk,
    input areset,

    output ack,
    input req,
    input load,
    input store,
    output [`WORD_SIZE - 1 : 0] out,
    input [`WORD_SIZE - 1 : 0] in,
    input [`WORD_SIZE - 1 : 0] addr
);
    reg [`WORD_SIZE - 1 : 0] buffer[(1 << `WORD_SIZE) - 1 : 0];
    reg [`IO_STATE_BITS - 1 : 0] state;
    wire [`IO_STATE_BITS - 1 : 0] next_state;

    initial reload_memory;
    always @(posedge clk) state <= next_state;
    always @(areset) if (areset) begin
        state <= `IO_WAITREQ;
        reload_memory;
    end

    assign next_state =
        state == `IO_WAITREQ && req ? `IO_DOWORK :
        state == `IO_DOWORK ? `IO_WAITACK :
        state == `IO_WAITACK && !req ? `IO_WAITREQ :
        state;

    assign ack = state == `IO_WAITACK;

    integer i;
    integer fd;
    integer ret;
    task reload_memory;
        begin
            fd = $fopen("memory.hex", "r");
            i = 0;
            ret = 1;
            while (ret == 1) begin
                ret = $fscanf(fd, "%h", buffer[i]);
                if (ret != 0) i = i + 1;
            end
            $fclose(fd);
            while (i < (1 << `WORD_SIZE)) begin
                buffer[i] = 0;
                i = i + 1;
            end
        end
    endtask

    always @(posedge clk) if (state == `IO_DOWORK && store) buffer[addr] <= in;

    assign out = load ? buffer[addr] : 0;
endmodule
