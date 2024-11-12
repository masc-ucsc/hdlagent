// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, in0, in1, in2, in3, out_o);
    input clk;
    input in0;
    input in1;
    input in2;
    input in3;
    output out_o;

    wire mid1;
    wire mid2;
    wire tmp0;
    wire tmp1;
    wire tmp2;

    // Combinational
    assign mid1 = tmp0;
    assign mid2 = tmp1;
    assign out_o = tmp2;
    assign tmp0 = in0 | in1;
    assign tmp1 = in2 | in3;
    assign tmp2 = mid1 | mid2;

endmodule

