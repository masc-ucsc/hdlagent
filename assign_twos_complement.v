// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, bin_input, complement_output);
    input clk;
    input[3:0] bin_input;
    output[3:0] complement_output;

    wire[3:0] const_0_15;
    wire[3:0] tmp0;

    // Combinational
    assign const_0_15 = 15;
    assign complement_output = tmp0;
    assign tmp0 = bin_input ^ const_0_15;

endmodule

