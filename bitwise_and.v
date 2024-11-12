// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, a, b, o);
    input clk;
    input[7:0] a;
    input[7:0] b;
    output[7:0] o;

    wire[7:0] tmp0;

    // Combinational
    assign o = tmp0;
    assign tmp0 = a & b;

endmodule

