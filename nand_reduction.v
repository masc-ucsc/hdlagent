// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, reduce_i, result_o);
    input clk;
    input[7:0] reduce_i;
    output result_o;

    wire intermediate_0;
    wire intermediate_1;
    wire intermediate_2;
    wire intermediate_3;
    wire intermediate_4;
    wire tmp0;
    wire tmp1;
    wire tmp2;
    wire tmp3;
    wire tmp4;
    wire tmp5;
    wire tmp6;
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

    // Combinational
    assign intermediate_0 = tmp3;
    assign intermediate_1 = tmp7;
    assign intermediate_2 = tmp11;
    assign intermediate_3 = tmp15;
    assign intermediate_4 = tmp17;
    assign result_o = tmp20;
    assign tmp0 = {reduce_i[0]};
    assign tmp1 = {reduce_i[1]};
    assign tmp2 = tmp0 & tmp1;
    assign tmp3 = ~tmp2;
    assign tmp4 = {reduce_i[2]};
    assign tmp5 = {reduce_i[3]};
    assign tmp6 = tmp4 & tmp5;
    assign tmp7 = ~tmp6;
    assign tmp8 = {reduce_i[4]};
    assign tmp9 = {reduce_i[5]};
    assign tmp10 = tmp8 & tmp9;
    assign tmp11 = ~tmp10;
    assign tmp12 = {reduce_i[6]};
    assign tmp13 = {reduce_i[7]};
    assign tmp14 = tmp12 & tmp13;
    assign tmp15 = ~tmp14;
    assign tmp16 = intermediate_0 & intermediate_1;
    assign tmp17 = ~tmp16;
    assign tmp18 = intermediate_2 & intermediate_3;
    assign tmp19 = tmp18 & intermediate_4;
    assign tmp20 = ~tmp19;

endmodule

