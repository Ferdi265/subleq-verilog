`include "defines.vh"

module subleq_controller(
    input clk,
    input areset,

    input ack,
    input halt,
    output [`STATE_BITS - 1 : 0] control_word
);
    reg [`STATE_BITS - 1 : 0] state;
    wire [`STATE_BITS - 1 : 0] next_state;

    always @(posedge clk) state <= next_state;
    always @(areset) if (areset) state <= `FETCH_A;

    assign next_state =
        halt ? `HALT :
        state == `FETCH_A && ack ? `WAIT_A :
        state == `WAIT_A && !ack ? `FINISH_A :
        state == `FINISH_A ? `DEREF_A :
        state == `DEREF_A && ack ? `WAIT_DA :
        state == `WAIT_DA && !ack ? `FETCH_B :
        state == `FETCH_B && ack ? `WAIT_B :
        state == `WAIT_B && !ack ? `FINISH_B :
        state == `FINISH_B ? `DEREF_B :
        state == `DEREF_B && ack ? `WAIT_DB :
        state == `WAIT_DB && !ack ? `STORE_SUB :
        state == `STORE_SUB && ack ? `WAIT_STORE :
        state == `WAIT_STORE && !ack ? `FETCH_C :
        state == `FETCH_C && ack ? `WAIT_C :
        state;

    assign control_word = state;
endmodule
