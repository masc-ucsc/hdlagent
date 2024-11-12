// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, rst, reset, state);
    input clk;
    input rst;
    input reset;
    output[1:0] state;

    reg[1:0] state_reg;

    wire[1:0] const_0_0;
    wire const_1_0;
    wire const_2_0;
    wire[1:0] const_3_1;
    wire const_4_1;
    wire const_5_0;
    wire[1:0] const_6_2;
    wire[1:0] const_7_2;
    wire[1:0] const_8_3;
    wire[1:0] const_9_3;
    wire[1:0] const_10_0;
    wire tmp0;
    wire[1:0] tmp1;
    wire tmp2;
    wire tmp3;
    wire tmp4;
    wire tmp5;
    wire[1:0] tmp6;
    wire tmp7;
    wire tmp8;
    wire tmp9;
    wire tmp10;
    wire tmp11;
    wire tmp12;
    wire tmp13;
    wire tmp14;
    wire tmp15;
    wire tmp16;
    wire tmp17;
    wire tmp18;
    wire tmp19;
    wire tmp20;
    wire tmp21;
    wire tmp22;
    wire tmp23;
    wire tmp24;
    wire tmp25;
    wire tmp26;
    wire tmp27;
    wire[1:0] tmp28;
    wire[1:0] tmp29;
    wire[1:0] tmp30;
    wire[1:0] tmp31;
    wire[1:0] tmp32;

    // Combinational
    assign const_0_0 = 0;
    assign const_1_0 = 0;
    assign const_2_0 = 0;
    assign const_3_1 = 1;
    assign const_4_1 = 1;
    assign const_5_0 = 0;
    assign const_6_2 = 2;
    assign const_7_2 = 2;
    assign const_8_3 = 3;
    assign const_9_3 = 3;
    assign const_10_0 = 0;
    assign state = state_reg;
    assign tmp0 = {const_2_0};
    assign tmp1 = {tmp0, const_1_0};
    assign tmp2 = state_reg == tmp1;
    assign tmp3 = ~reset;
    assign tmp4 = tmp3 & tmp2;
    assign tmp5 = {const_5_0};
    assign tmp6 = {tmp5, const_4_1};
    assign tmp7 = state_reg == tmp6;
    assign tmp8 = ~reset;
    assign tmp9 = ~tmp2;
    assign tmp10 = tmp8 & tmp9;
    assign tmp11 = tmp10 & tmp7;
    assign tmp12 = state_reg == const_7_2;
    assign tmp13 = ~reset;
    assign tmp14 = ~tmp2;
    assign tmp15 = tmp13 & tmp14;
    assign tmp16 = ~tmp7;
    assign tmp17 = tmp15 & tmp16;
    assign tmp18 = tmp17 & tmp12;
    assign tmp19 = state_reg == const_9_3;
    assign tmp20 = ~reset;
    assign tmp21 = ~tmp2;
    assign tmp22 = tmp20 & tmp21;
    assign tmp23 = ~tmp7;
    assign tmp24 = tmp22 & tmp23;
    assign tmp25 = ~tmp12;
    assign tmp26 = tmp24 & tmp25;
    assign tmp27 = tmp26 & tmp19;
    assign tmp28 = reset ? const_0_0 : state_reg;
    assign tmp29 = tmp4 ? const_3_1 : tmp28;
    assign tmp30 = tmp11 ? const_6_2 : tmp29;
    assign tmp31 = tmp18 ? const_8_3 : tmp30;
    assign tmp32 = tmp27 ? const_10_0 : tmp31;

    // Registers
    always @(posedge clk)
    begin
        if (rst) begin
            state_reg <= 0;
        end
        else begin
            state_reg <= tmp32;
        end
    end

endmodule

