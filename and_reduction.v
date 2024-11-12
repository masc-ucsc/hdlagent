// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, reduce_i, result_o);
    input clk;
    input[7:0] reduce_i;
    output result_o;

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
    assign result_o = tmp14;
    assign result_o = tmp17;
    assign result_o = tmp8;
    assign result_o = tmp20;
    assign result_o = tmp11;
    assign result_o = tmp2;
    assign result_o = tmp5;
    assign tmp0 = {reduce_i[0]};
    assign tmp1 = {reduce_i[1]};
    assign tmp2 = tmp0 & tmp1;
    assign tmp3 = {reduce_i[1]};
    assign tmp4 = {reduce_i[2]};
    assign tmp5 = tmp3 & tmp4;
    assign tmp6 = {reduce_i[2]};
    assign tmp7 = {reduce_i[3]};
    assign tmp8 = tmp6 & tmp7;
    assign tmp9 = {reduce_i[3]};
    assign tmp10 = {reduce_i[4]};
    assign tmp11 = tmp9 & tmp10;
    assign tmp12 = {reduce_i[4]};
    assign tmp13 = {reduce_i[5]};
    assign tmp14 = tmp12 & tmp13;
    assign tmp15 = {reduce_i[5]};
    assign tmp16 = {reduce_i[6]};
    assign tmp17 = tmp15 & tmp16;
    assign tmp18 = {reduce_i[6]};
    assign tmp19 = {reduce_i[7]};
    assign tmp20 = tmp18 & tmp19;

endmodule

