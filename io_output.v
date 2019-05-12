`include "defines.vh"

module io_output(
    output ack,
    input req,
    input [`WORD_SIZE - 1 : 0] data
);
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

    always @(posedge req) $fwrite(fd, "%s", data[7 : 0]);
    assign ack = req;
endmodule
