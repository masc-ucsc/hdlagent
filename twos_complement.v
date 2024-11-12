// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, bin_input, complement_output);
    input clk;
    input[3:0] bin_input;
    output[3:0] complement_output;

    wire[14:0] const_0_4;
    wire const_1_0;
    wire const_2_1;
    wire const_3_0;
    wire[10:0] tmp0;
    wire[14:0] tmp1;
    wire[14:0] tmp2;
    wire[13:0] tmp3;
    wire[14:0] tmp4;
    wire[15:0] tmp5;
    wire[3:0] tmp6;

    // Combinational
    assign const_0_4 = 4;
    assign const_1_0 = 0;
    assign const_2_1 = 1;
    assign const_3_0 = 0;
    assign complement_output = tmp6;
    assign tmp0 = {const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0};
    assign tmp1 = {tmp0, bin_input};
    assign tmp2 = tmp1 ^ const_0_4;
    assign tmp3 = {const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0};
    assign tmp4 = {tmp3, const_2_1};
    assign tmp5 = tmp2 + tmp4;
    assign tmp6 = {tmp5[3], tmp5[2], tmp5[1], tmp5[0]};

endmodule

