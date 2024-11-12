// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, a, result);
    input clk;
    input[7:0] a;
    output[7:0] result;


    // Combinational
    assign result = a;

endmodule

