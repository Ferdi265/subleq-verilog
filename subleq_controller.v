`include "defines.vh"

module subleq_controller(
    input clk,
    input areset,

    input halt,
    output [`STATE_BITS - 1 : 0] control_word
);
    wire clk;
    wire areset;

    wire halt;
    wire [`STATE_BITS - 1 : 0] control_word;

    reg [`STATE_BITS - 1 : 0] state;
    wire [`STATE_BITS - 1 : 0] next_state;

    always @(posedge clk) state <= next_state;
    always @(areset) if (areset) state <= `FETCH_A;

    assign next_state =
        halt ? `HALT :
        state == `FETCH_A ? `DEREF_A :
        state == `DEREF_A ? `FETCH_B :
        state == `FETCH_B ? `DEREF_B :
        state == `DEREF_B ? `STORE_SUB :
        state == `STORE_SUB ? `FETCH_C :
        state == `FETCH_C ? `FETCH_A :
        state;

    assign control_word = state;
endmodule
