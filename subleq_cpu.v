`include "defines.vh"

module subleq_cpu(
    input clk,
    input areset,

    input halt,
    output load,
    input [`WORD_SIZE - 1 : 0] data_in,
    output [`WORD_SIZE - 1 : 0] data_out,
    output [`WORD_SIZE - 1 : 0] addr
);
    wire [`WORD_SIZE - 1 : 0] data_in_0;
    wire [`WORD_SIZE - 1 : 0] data_in_1;
    wire [`WORD_SIZE - 1 : 0] data_in_2;
    wire [`WORD_SIZE - 1 : 0] pc_addr;
    wire [`WORD_SIZE - 1 : 0] a_value;

    wire [`STATE_BITS - 1 : 0] control_word;
    wire leq;
    wire branch;
    wire inc;
    wire set;

    wire fetch;
    wire deref;

    data_in_buffer dinbuf(clk, areset, data_in, data_in_0, data_in_1, data_in_2);
    a_register areg(clk, areset, set, data_in_1, a_value);

    subleq_controller ctrl(clk, areset, halt, control_word);
    subleq_pc pc(clk, areset, branch, inc, data_in_0, pc_addr);

    assign fetch = control_word == `FETCH_A || control_word == `FETCH_B || control_word == `FETCH_C;
    assign deref = control_word == `DEREF_A || control_word == `DEREF_B;
    assign load = control_word != `STORE_SUB;

    assign addr =
        control_word == `HALT ? (1 << `WORD_SIZE) - 1 :
        deref ? data_in_1 :
        fetch ? pc_addr :
        data_in_2;

    assign data_out = data_in_1 - a_value;
    assign leq = !($signed(data_in_2 - a_value) > $signed(0));
    assign branch = control_word == `FETCH_C && leq;
    assign inc = fetch;
    assign set = control_word == `FETCH_B;
endmodule
