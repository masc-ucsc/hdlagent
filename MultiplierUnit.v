// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, recv_msg, recv_val, send_rdy, recv_rdy, send_msg, send_val);
    input clk;
    input[63:0] recv_msg;
    input recv_val;
    input send_rdy;
    output recv_rdy;
    output[31:0] send_msg;
    output send_val;

    wire[31:0] tmp0;
    wire[31:0] tmp1;
    wire[63:0] tmp2;
    wire[31:0] tmp3;

    // Combinational
    assign recv_rdy = send_rdy;
    assign send_msg = tmp3;
    assign send_val = send_rdy;
    assign tmp0 = {recv_msg[31], recv_msg[30], recv_msg[29], recv_msg[28], recv_msg[27], recv_msg[26], recv_msg[25], recv_msg[24], recv_msg[23], recv_msg[22], recv_msg[21], recv_msg[20], recv_msg[19], recv_msg[18], recv_msg[17], recv_msg[16], recv_msg[15], recv_msg[14], recv_msg[13], recv_msg[12], recv_msg[11], recv_msg[10], recv_msg[9], recv_msg[8], recv_msg[7], recv_msg[6], recv_msg[5], recv_msg[4], recv_msg[3], recv_msg[2], recv_msg[1], recv_msg[0]};
    assign tmp1 = {recv_msg[63], recv_msg[62], recv_msg[61], recv_msg[60], recv_msg[59], recv_msg[58], recv_msg[57], recv_msg[56], recv_msg[55], recv_msg[54], recv_msg[53], recv_msg[52], recv_msg[51], recv_msg[50], recv_msg[49], recv_msg[48], recv_msg[47], recv_msg[46], recv_msg[45], recv_msg[44], recv_msg[43], recv_msg[42], recv_msg[41], recv_msg[40], recv_msg[39], recv_msg[38], recv_msg[37], recv_msg[36], recv_msg[35], recv_msg[34], recv_msg[33], recv_msg[32]};
    assign tmp2 = tmp0 * tmp1;
    assign tmp3 = {tmp2[31], tmp2[30], tmp2[29], tmp2[28], tmp2[27], tmp2[26], tmp2[25], tmp2[24], tmp2[23], tmp2[22], tmp2[21], tmp2[20], tmp2[19], tmp2[18], tmp2[17], tmp2[16], tmp2[15], tmp2[14], tmp2[13], tmp2[12], tmp2[11], tmp2[10], tmp2[9], tmp2[8], tmp2[7], tmp2[6], tmp2[5], tmp2[4], tmp2[3], tmp2[2], tmp2[1], tmp2[0]};

endmodule

