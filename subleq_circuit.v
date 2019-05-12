`include "defines.vh"

module subleq_circuit(
    input clk,
    input areset
);
    wire eof;
    wire in_ack;
    wire in_req;
    wire out_ack;
    wire out_req;
    wire [`WORD_SIZE - 1 : 0] io_in;
    wire [`WORD_SIZE - 1 : 0] io_out;

    wire mem_ack;
    wire mem_req;
    wire mem_load;
    wire mem_store;
    wire [`WORD_SIZE - 1 : 0] mem_out;
    wire [`WORD_SIZE - 1 : 0] mem_in;
    wire [`WORD_SIZE - 1 : 0] mem_addr;

    wire cpu_ack;
    wire cpu_req;
    wire cpu_halt;
    wire cpu_load;
    wire cpu_store;
    wire [`WORD_SIZE - 1 : 0] data_in;
    wire [`WORD_SIZE - 1 : 0] data_out;
    wire [`WORD_SIZE - 1 : 0] addr;

    io_input in(
        clk, areset,

        eof, in_ack, in_req, io_in
    );
    io_output out(
        clk, areset,

        out_ack, out_req, io_out
    );
    memory mem(
        areset,

        mem_ack, mem_req,
        mem_load, mem_store,
        mem_out, mem_in, mem_addr
    );
    subleq_cpu cpu(
        clk, areset,

        cpu_ack, cpu_req,
        cpu_halt, cpu_load, cpu_store,
        data_in, data_out, addr
    );
    subleq_mmio mmio(
        eof, in_ack, in_req, io_in,
        out_ack, out_req, io_out,

        cpu_ack, cpu_req,
        cpu_halt, cpu_load, cpu_store,
        data_in, data_out, addr,

        mem_ack, mem_req,
        mem_load, mem_store,
        mem_out, mem_in, mem_addr
    );
endmodule
