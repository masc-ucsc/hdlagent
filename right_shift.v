// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, a, o);
    input clk;
    input[7:0] a;
    output[7:0] o;

    wire const_0_0;
    wire[4:0] tmp0;
    wire[2:0] tmp1;
    wire[7:0] tmp2;

    // Combinational
    assign const_0_0 = 0;
    assign o = tmp2;
    assign tmp0 = {a[7], a[6], a[5], a[4], a[3]};
    assign tmp1 = {const_0_0, const_0_0, const_0_0};
    assign tmp2 = {tmp1, tmp0};

endmodule

