`include "defines.vh"

module subleq_cpu(
    input clk,
    input areset,

    input ack,
    output req,
    input halt,
    output load,
    output store,
    input signed [`WORD_SIZE - 1 : 0] data_in,
    output signed [`WORD_SIZE - 1 : 0] data_out,
    output [`WORD_SIZE - 1 : 0] addr
);
    reg signed [`WORD_SIZE - 1 : 0] a;
    reg signed [`WORD_SIZE - 1 : 0] b;
    reg [`WORD_SIZE - 1 : 0] ptr;
    reg [`WORD_SIZE - 1 : 0] pc;

    wire [`STATE_BITS - 1 : 0] control_word;
    wire leq;

    subleq_controller ctrl(clk, areset, ack, halt, control_word);

    always @(posedge clk) case (control_word)
        `FETCH_A: ptr <= data_in;
        `FETCH_B: ptr <= data_in;
        `FETCH_C: ptr <= data_in;
        `DEREF_A: a <= data_in;
        `DEREF_B: b <= data_in;
        `BRANCH: pc <= (leq ? ptr : pc + 3);
    endcase

    always @(areset) if (areset) begin
        a <= 0;
        b <= 0;
        ptr <= 0;
        pc <= 0;
    end

    assign addr =
        control_word == `HALT ? (1 << `WORD_SIZE) - 1 :
        control_word == `FETCH_A ? pc :
        control_word == `WAIT_A ? pc :
        control_word == `FETCH_B ? pc + 1 :
        control_word == `WAIT_B ? pc + 1 :
        control_word == `FETCH_C ? pc + 2 :
        control_word == `WAIT_C ? pc + 2 :
        control_word == `DEREF_A ? ptr :
        control_word == `WAIT_DA ? ptr :
        control_word == `DEREF_B ? ptr :
        control_word == `WAIT_DB ? ptr :
        control_word == `STORE_SUB ? ptr :
        control_word == `WAIT_STORE ? ptr :
        0;

    assign req =
        control_word == `FETCH_A ||
        control_word == `FETCH_B ||
        control_word == `FETCH_C ||
        control_word == `DEREF_A ||
        control_word == `DEREF_B ||
        control_word == `STORE_SUB;

    assign load =
        control_word == `FETCH_A ||
        control_word == `FETCH_B ||
        control_word == `FETCH_C ||
        control_word == `DEREF_A ||
        control_word == `DEREF_B ||
        control_word == `WAIT_A ||
        control_word == `WAIT_B ||
        control_word == `WAIT_C ||
        control_word == `WAIT_DA ||
        control_word == `WAIT_DB;
    assign store =
        control_word == `STORE_SUB ||
        control_word == `WAIT_STORE;

    assign data_out = b - a;
    assign leq = data_out <= 0;
endmodule
