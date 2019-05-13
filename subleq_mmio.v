`include "defines.vh"

module subleq_mmio(
    input eof,
    input in_ack,
    output in_req,
    input [`WORD_SIZE - 1 : 0] io_in,

    input out_ack,
    output out_req,
    output [`WORD_SIZE - 1 : 0] io_out,

    output cpu_ack,
    input cpu_req,
    output cpu_halt,
    input cpu_load,
    input cpu_store,
    output [`WORD_SIZE - 1 : 0] data_in,
    input [`WORD_SIZE - 1 : 0] data_out,
    input [`WORD_SIZE - 1 : 0] addr,

    input mem_ack,
    output mem_req,
    output mem_load,
    output mem_store,
    input [`WORD_SIZE - 1 : 0] mem_out,
    output [`WORD_SIZE - 1 : 0] mem_in,
    output [`WORD_SIZE - 1 : 0] mem_addr
);
    wire addr_io;
    wire addr_io_halt;
    wire addr_io_write;
    wire addr_io_read;

    // ADDR CASES
    assign addr_io = addr >= ((1 << `WORD_SIZE) - 3);
    assign addr_io_halt = addr == ((1 << `WORD_SIZE) - 1);
    assign addr_io_write = addr == ((1 << `WORD_SIZE) - 2);
    assign addr_io_read = addr == ((1 << `WORD_SIZE) - 3);

    // INPUT
    wire in_read;
    assign in_read = addr_io_read && cpu_load;
    assign in_req = in_read ? cpu_req : 0;

    // OUTPUT
    wire out_write;
    assign out_write = addr_io_write && cpu_store;
    assign out_req = out_write ? cpu_req : 0;
    assign io_out = out_write ? data_out : 0;

    // MEMORY
    assign mem_req = !addr_io ? cpu_req : 0;
    assign mem_load = !addr_io ? cpu_load : 0;
    assign mem_store = !addr_io ? cpu_store : 0;
    assign mem_in = !addr_io ? data_out : 0;
    assign mem_addr = !addr_io ? addr : 0;

    // CPU
    assign cpu_ack =
        !addr_io ? mem_ack :
        in_read ? in_ack :
        out_write ? out_ack :
        cpu_req;
    assign cpu_halt = (eof && in_read) || addr_io_halt;
    assign data_in =
        !addr_io ? mem_out :
        in_read ? io_in :
        0;
endmodule
