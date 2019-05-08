`include "defines.vh"

module test;
    reg clk, areset;

    initial clk = 0;
    always #5 clk = !clk;

    subleq_circuit subl(clk, areset);

    initial begin
        areset = 1;
        #1
        areset = 0;
        #9
        areset = 1;
        #1
        areset = 0;
        #9

        wait (subl.cpu.ctrl.state == `HALT);
        $finish;
    end

    task dump;
        input [`WORD_SIZE - 1 : 0] start_addr;
        input [`WORD_SIZE - 1 : 0] end_addr;
        begin
            for (i = start_addr; i < end_addr; i = i + 16) begin
                $write("  %04h:", i);
                for (j = 0; j < 16 && i + j < end_addr; j = j + 1) begin
                    $write(" %04h", subl.mem.buffer[i + j]);
                end
                $display("");
            end
        end
    endtask

    reg [`WORD_SIZE - 1 : 0] i;
    reg [`WORD_SIZE - 1 : 0] j;
    always @(clk) begin
        $display("[TIME = %t] CLK = %h, ARESET = %h", $time, clk, areset);
        if (clk) begin
            $display("MEMORY:");
            dump(0, 256);
            $write("STATE = ");
            case (subl.cpu.ctrl.state)
                `FETCH_A: $write("FETCH_A  ");
                `DEREF_A: $write("DEREF_A  ");
                `FETCH_B: $write("FETCH_B  ");
                `DEREF_B: $write("DEREF_B  ");
                `STORE_SUB: $write("STORE_SUB");
                `FETCH_C: $write("FETCH_C  ");
                `HALT: $write("HALT     ");
                default: $write("????????");
            endcase
            $display("");
            $display("INTERNALS:");
            $display("  A = %h, PC = %h, ADDR = %h", subl.cpu.areg.a, subl.cpu.pc_addr, subl.cpu.addr);
            $display("  DIN = [%h, %h, %h], DOUT = %h", subl.cpu.data_in_0, subl.cpu.data_in_1, subl.cpu.data_in_2, subl.cpu.data_out);
            $display("  fetch = %h, deref = %h, load = %h", subl.cpu.fetch, subl.cpu.deref, subl.cpu.load);
            $display("  leq = %h, branch = %h, inc = %h, set = %h", subl.cpu.leq, subl.cpu.branch, subl.cpu.inc, subl.cpu.set);
        end
    end
endmodule
