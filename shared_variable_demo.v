// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, a);
    input clk;
    input[7:0] a;

    wire[7:0] o;
    wire[7:0] shared_var;

    // Combinational
    assign o = shared_var;
    assign shared_var = a;

endmodule

