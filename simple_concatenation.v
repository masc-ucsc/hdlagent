// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, a_i, b_i, result_o);
    input clk;
    input[7:0] a_i;
    input[7:0] b_i;
    output[15:0] result_o;

    wire[15:0] tmp0;

    // Combinational
    assign result_o = tmp0;
    assign tmp0 = {a_i, b_i};

endmodule

