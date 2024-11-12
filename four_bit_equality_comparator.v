// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, A, B, equality, val_o);
    input clk;
    input[3:0] A;
    input[3:0] B;
    output equality;
    output[3:0] val_o;

    wire tmp0;
    wire tmp1;
    wire[3:0] tmp2;

    // Combinational
    assign tmp0 = A == B;
    assign tmp1 = A > B;
    assign tmp2 = tmp1 ? A : B;

endmodule

