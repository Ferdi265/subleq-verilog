`include "defines.vh"

module subleq_circuit(
    input clk,
    input areset
);
    wire in_avail;
    wire in_read;
    wire out_write;
    wire [`WORD_SIZE - 1 : 0] io_in;
    wire [`WORD_SIZE - 1 : 0] io_out;

    wire load;
    wire store;
    wire [`WORD_SIZE - 1 : 0] mem_out;
    wire [`WORD_SIZE - 1 : 0] mem_in;
    wire [`WORD_SIZE - 1 : 0] mem_addr;

    wire halt;
    wire [`WORD_SIZE - 1 : 0] data_in;
    wire [`WORD_SIZE - 1 : 0] data_out;
    wire [`WORD_SIZE - 1 : 0] addr;

    io_input io_i(clk, areset, in_avail, in_read, io_in);
    io_output io_o(clk, areset, out_write, io_out);
    memory mem(clk, areset, load, store, mem_out, mem_in, mem_addr);
    mmio mmapped_io(in_avail, in_read, out_write, io_in, io_out, halt, load, data_in, data_out, addr, mem_out, mem_in, mem_addr);
    subleq_cpu cpu(clk, areset, halt, load, data_in, data_out, addr);

    assign store = !load;
endmodule
