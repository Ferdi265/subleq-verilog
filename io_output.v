`include "defines.vh"

module io_output(
    input clk,
    input areset,

    input out_write,
    input [`WORD_SIZE - 1 : 0] io_out
);
    wire clk;
    wire areset;

    wire out_write;
    wire [`WORD_SIZE - 1 : 0] io_out;

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

    always @(posedge clk) if (out_write) begin
        $fwrite(fd, "%s", io_out[7 : 0]);
    end
endmodule
