`include "defines.vh"

module subleq_circuit(
    input clk,
    input areset,

    input in_eof,
    input in_ack,
    output in_req,
    input [`WORD_SIZE - 1 : 0] in_data,

    input out_ack,
    output out_req,
    output [`WORD_SIZE - 1 : 0] out_data
);
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

    memory mem(
        clk, areset,

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
        in_eof, in_ack, in_req, in_data,
        out_ack, out_req, out_data,

        cpu_ack, cpu_req,
        cpu_halt, cpu_load, cpu_store,
        data_in, data_out, addr,

        mem_ack, mem_req,
        mem_load, mem_store,
        mem_out, mem_in, mem_addr
    );
endmodule
