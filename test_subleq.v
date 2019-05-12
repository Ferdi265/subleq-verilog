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

        wait (subl.cpu.ctrl.state == `HALT);
        if ($test$plusargs("autotest")) begin
            dump(16'h000, (1 << `WORD_SIZE) - 1);
        end
        $finish;
    end

    integer i;
    integer j;
    task dump;
        input [`WORD_SIZE - 1 : 0] start_addr;
        input [`WORD_SIZE - 1 : 0] end_addr;
        begin
            for (i = start_addr; i <= end_addr; i = i + 16) begin
                $write("  %04h:", i[`WORD_SIZE - 1 : 0]);
                for (j = 0; j < 16 && i + j <= end_addr; j = j + 1) begin
                    $write(" %04h", subl.mem.buffer[i + j]);
                end
                $display("");
            end
        end
    endtask

    always @(clk) if ($test$plusargs("debug")) begin
        $display("[TIME = %t] CLK = %h, ARESET = %h", $time, clk, areset);
        if (clk) begin
            $write("STATE = ");
            case (subl.cpu.ctrl.state)
                `FETCH_A:       $write("FETCH_A   ");
                `WAIT_A:        $write("WAIT_A    ");
                `DEREF_A:       $write("DEREF_A   ");
                `WAIT_DA:       $write("WAIT_DA   ");
                `FETCH_B:       $write("FETCH_B   ");
                `WAIT_B:        $write("WAIT_B    ");
                `DEREF_B:       $write("DEREF_B   ");
                `WAIT_DB:       $write("WAIT_DB   ");
                `STORE_SUB:     $write("STORE_SUB ");
                `WAIT_STORE:    $write("WAIT_STORE");
                `FETCH_C:       $write("FETCH_C   ");
                `WAIT_C:        $write("WAIT_C    ");
                `BRANCH:        $write("BRANCH    ");
                `HALT:          $write("HALT      ");
                default:        $write("??????????");
            endcase
            $write(", NEXT_STATE = ");
            case (subl.cpu.ctrl.next_state)
                `FETCH_A:       $write("FETCH_A   ");
                `WAIT_A:        $write("WAIT_A    ");
                `DEREF_A:       $write("DEREF_A   ");
                `WAIT_DA:       $write("WAIT_DA   ");
                `FETCH_B:       $write("FETCH_B   ");
                `WAIT_B:        $write("WAIT_B    ");
                `DEREF_B:       $write("DEREF_B   ");
                `WAIT_DB:       $write("WAIT_DB   ");
                `STORE_SUB:     $write("STORE_SUB ");
                `WAIT_STORE:    $write("WAIT_STORE");
                `FETCH_C:       $write("FETCH_C   ");
                `WAIT_C:        $write("WAIT_C    ");
                `BRANCH:        $write("BRANCH    ");
                `HALT:          $write("HALT      ");
                default:        $write("??????????");
            endcase
            $display("");
            $display("CPU INTERNALS:");
            $display("  A = %h, B = %h, PTR = %h, PC = %h, ADDR = %h", subl.cpu.a, subl.cpu.b, subl.cpu.ptr, subl.cpu.pc, subl.cpu.addr);
            $display("  DIN = %h, DOUT = %h, REQ = %h, ACK = %h", subl.cpu.data_in, subl.cpu.data_out, subl.cpu.req, subl.cpu.ack);
            $display("  load = %h, store = %h, halt = %h, leq = %h", subl.cpu.load, subl.cpu.store, subl.cpu.halt, subl.cpu.leq);
            $display("MMIO INTERNALS:");
            $display("  input:  REQ = %h, ACK = %h, eof = %h, data = %h", subl.in.req, subl.in.ack, subl.in.eof, subl.in.data);
            $display("  output: REQ = %h, ACK = %h, data = %h", subl.out.req, subl.out.ack, subl.out.data);
            $display("  memory: REQ = %h, ACK = %h, load = %h, store = %h, addr = %h, in = %h, out = %h", subl.mem.req, subl.mem.ack, subl.mem.load, subl.mem.store, subl.mem.addr, subl.mem.in, subl.mem.out);

            $display("MEMORY 0000 - 0080:");
            dump(16'h0000, 16'h007f);
        end
    end
endmodule
