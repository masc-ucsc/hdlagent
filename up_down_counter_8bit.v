// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, rst, reset, up_down, out_o);
    input clk;
    input rst;
    input reset;
    input up_down;
    output[7:0] out_o;

    reg[7:0] _ver_out_tmp_0;

    wire const_0_1;
    wire const_1_0;
    wire const_2_1;
    wire const_3_0;
    wire tmp0;
    wire[6:0] tmp1;
    wire[7:0] tmp2;
    wire[8:0] tmp3;
    wire[7:0] tmp4;
    wire tmp5;
    wire tmp6;
    wire[6:0] tmp7;
    wire[7:0] tmp8;
    wire[8:0] tmp9;
    wire[7:0] tmp10;
    wire tmp11;
    wire tmp12;
    wire[7:0] tmp13;
    wire[7:0] tmp14;

    // Combinational
    assign const_0_1 = 1;
    assign const_1_0 = 0;
    assign const_2_1 = 1;
    assign const_3_0 = 0;
    assign out_o = _ver_out_tmp_0;
    assign tmp0 = reset | up_down;
    assign tmp1 = {const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0, const_1_0};
    assign tmp2 = {tmp1, const_0_1};
    assign tmp3 = _ver_out_tmp_0 + tmp2;
    assign tmp4 = {tmp3[7], tmp3[6], tmp3[5], tmp3[4], tmp3[3], tmp3[2], tmp3[1], tmp3[0]};
    assign tmp5 = ~up_down;
    assign tmp6 = reset & tmp5;
    assign tmp7 = {const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0, const_3_0};
    assign tmp8 = {tmp7, const_2_1};
    assign tmp9 = _ver_out_tmp_0 - tmp8;
    assign tmp10 = {tmp9[7], tmp9[6], tmp9[5], tmp9[4], tmp9[3], tmp9[2], tmp9[1], tmp9[0]};
    assign tmp11 = ~tmp0;
    assign tmp12 = tmp11 & tmp6;
    assign tmp13 = tmp0 ? tmp4 : _ver_out_tmp_0;
    assign tmp14 = tmp12 ? tmp10 : tmp13;

    // Registers
    always @(posedge clk)
    begin
        if (rst) begin
            _ver_out_tmp_0 <= 0;
        end
        else begin
            _ver_out_tmp_0 <= tmp14;
        end
    end

endmodule

