// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, binary_input, gray_code);
    input clk;
    input[3:0] binary_input;
    output[3:0] gray_code;

    wire const_0_0;
    wire[2:0] tmp0;
    wire[3:0] tmp1;
    wire[3:0] tmp2;

    // Combinational
    assign const_0_0 = 0;
    assign gray_code = tmp2;
    assign tmp0 = {binary_input[2], binary_input[1], binary_input[0]};
    assign tmp1 = {const_0_0, tmp0};
    assign tmp2 = binary_input ^ tmp1;

endmodule

