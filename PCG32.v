// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, rst, _ver_out_tmp_0);
    input clk;
    input rst;
    output[31:0] _ver_out_tmp_0;

    reg[31:0] state_0;
    reg[31:0] state_1;

    wire const_0_1;
    wire const_1_0;
    wire[30:0] const_2_1640531527;
    wire const_3_0;
    wire const_4_0;
    wire[31:0] const_5_3605559197;
    wire const_6_0;
    wire const_7_0;
    wire const_8_0;
    wire[31:0] inc;
    wire[31:0] output_gen;
    wire[30:0] tmp0;
    wire[31:0] tmp1;
    wire[32:0] tmp2;
    wire[31:0] tmp3;
    wire tmp4;
    wire[31:0] tmp5;
    wire[63:0] tmp6;
    wire[31:0] tmp7;
    wire[63:0] tmp8;
    wire[64:0] tmp9;
    wire[63:0] tmp10;
    wire[31:0] tmp11;
    wire[63:0] tmp12;
    wire[64:0] tmp13;
    wire[31:0] tmp14;
    wire[31:0] tmp15;
    wire[13:0] tmp16;
    wire[17:0] tmp17;
    wire[31:0] tmp18;
    wire[3:0] tmp19;
    wire[27:0] tmp20;
    wire[31:0] tmp21;
    wire[31:0] tmp22;
    wire[31:0] tmp23;

    // Combinational
    assign const_0_1 = 1;
    assign const_1_0 = 0;
    assign const_2_1640531527 = 1640531527;
    assign const_3_0 = 0;
    assign const_4_0 = 0;
    assign const_5_3605559197 = 3605559197;
    assign const_6_0 = 0;
    assign const_7_0 = 0;
    assign const_8_0 = 0;
    assign inc = tmp3;
    assign output_gen = tmp23;
    assign tmp0 = {const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0};
    assign tmp1 = {tmp0, const_0_1};
    assign tmp2 = state_0 + tmp1;
    assign tmp3 = {tmp2[31], tmp2[30], tmp2[29], tmp2[28], tmp2[27], tmp2[26], tmp2[25], tmp2[24], tmp2[23], tmp2[22], tmp2[21], tmp2[20], tmp2[19], tmp2[18], tmp2[17], tmp2[16], tmp2[15], tmp2[14], tmp2[13], tmp2[12], tmp2[11], tmp2[10], tmp2[9], tmp2[8], tmp2[7], tmp2[6], tmp2[5], tmp2[4], tmp2[3], tmp2[2], tmp2[1], tmp2[0]};
    assign tmp4 = {const_3_0};
    assign tmp5 = {tmp4, const_2_1640531527};
    assign tmp6 = state_0 * tmp5;
    assign tmp7 = {const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0, const_4_0};
    assign tmp8 = {tmp7, state_1};
    assign tmp9 = tmp6 + tmp8;
    assign tmp10 = state_1 * const_5_3605559197;
    assign tmp11 = {const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0, const_6_0};
    assign tmp12 = {tmp11, inc};
    assign tmp13 = tmp10 + tmp12;
    assign tmp14 = {tmp9[31], tmp9[30], tmp9[29], tmp9[28], tmp9[27], tmp9[26], tmp9[25], tmp9[24], tmp9[23], tmp9[22], tmp9[21], tmp9[20], tmp9[19], tmp9[18], tmp9[17], tmp9[16], tmp9[15], tmp9[14], tmp9[13], tmp9[12], tmp9[11], tmp9[10], tmp9[9], tmp9[8], tmp9[7], tmp9[6], tmp9[5], tmp9[4], tmp9[3], tmp9[2], tmp9[1], tmp9[0]};
    assign tmp15 = {tmp13[31], tmp13[30], tmp13[29], tmp13[28], tmp13[27], tmp13[26], tmp13[25], tmp13[24], tmp13[23], tmp13[22], tmp13[21], tmp13[20], tmp13[19], tmp13[18], tmp13[17], tmp13[16], tmp13[15], tmp13[14], tmp13[13], tmp13[12], tmp13[11], tmp13[10], tmp13[9], tmp13[8], tmp13[7], tmp13[6], tmp13[5], tmp13[4], tmp13[3], tmp13[2], tmp13[1], tmp13[0]};
    assign tmp16 = {state_0[31], state_0[30], state_0[29], state_0[28], state_0[27], state_0[26], state_0[25], state_0[24], state_0[23], state_0[22], state_0[21], state_0[20], state_0[19], state_0[18]};
    assign tmp17 = {const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0, const_7_0};
    assign tmp18 = {tmp17, tmp16};
    assign tmp19 = {state_0[31], state_0[30], state_0[29], state_0[28]};
    assign tmp20 = {const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0, const_8_0};
    assign tmp21 = {tmp20, tmp19};
    assign tmp22 = tmp18 ^ tmp21;
    assign tmp23 = tmp22 ^ state_1;

    // Registers
    always @(posedge clk or posedge rst)
    begin
        if (rst) begin
            state_0 <= 0;
            state_1 <= 0;
        end
        else begin
            state_0 <= tmp14;
            state_1 <= tmp15;
        end
    end

endmodule

