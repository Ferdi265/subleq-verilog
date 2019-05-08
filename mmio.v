`include "defines.vh"

module mmio(
    input eof,
    output in_read,
    output out_write,
    input [`WORD_SIZE - 1 : 0] io_in,
    output [`WORD_SIZE - 1 : 0] io_out,

    output halt,
    input load,
    output [`WORD_SIZE - 1 : 0] data_in,
    input [`WORD_SIZE - 1 : 0] data_out,
    input [`WORD_SIZE - 1 : 0] addr,

    input [`WORD_SIZE - 1 : 0] mem_out,
    output [`WORD_SIZE - 1 : 0] mem_in,
    output [`WORD_SIZE - 1 : 0] addr_out
);
    wire eof;
    wire in_read;
    wire out_write;
    wire [`WORD_SIZE - 1 : 0] io_in;
    wire [`WORD_SIZE - 1 : 0] io_out;

    wire halt;
    wire load;
    wire [`WORD_SIZE - 1 : 0] data_in;
    wire [`WORD_SIZE - 1 : 0] data_out;
    wire [`WORD_SIZE - 1 : 0] addr;

    wire [`WORD_SIZE - 1 : 0] mem_out;
    wire [`WORD_SIZE - 1 : 0] mem_in;
    wire [`WORD_SIZE - 1 : 0] addr_out;

    wire addr_io;
    wire addr_io_read;
    wire addr_io_write;

    assign addr_io = addr >= ((1 << `WORD_SIZE) - 3);
    assign addr_io_halt = addr == ((1 << `WORD_SIZE) - 1);
    assign addr_io_write = addr == ((1 << `WORD_SIZE) - 2);
    assign addr_io_read = addr == ((1 << `WORD_SIZE) - 3);
    assign addr_out = addr;

    assign in_read = addr_io_read && load;
    assign out_write = addr_io_write && !load;
    assign halt = (eof && in_read) || addr_io_halt;

    assign mem_in = addr_io ? 0 : data_out;
    assign io_out = out_write ? data_out : 0;
    assign data_in =
        !addr_io ? mem_out :
        in_read ? io_in :
        0;
endmodule
