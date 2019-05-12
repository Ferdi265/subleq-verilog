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
    reg [`WORD_SIZE - 1 : 0] buffer[(1 << `WORD_SIZE) - 1 : 0];

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

    initial reload_memory;
    always @(posedge areset) reload_memory;
    always @(posedge clk) if (store) buffer[addr] <= mem_in;

    assign mem_out = load ? buffer[addr] : 0;
endmodule
