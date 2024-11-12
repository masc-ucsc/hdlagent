// Generated automatically via PyRTL
// As one initial test of synthesis, map to FPGA with:
//   yosys -p "synth_xilinx -top toplevel" thisfile.v

module toplevel(clk, data_in, parity_out);
    input clk;
    input[3:0] data_in;
    output parity_out;

    wire tmp0;
    wire tmp1;
    wire tmp2;
    wire tmp3;
    wire tmp4;
    wire tmp5;
    wire tmp6;

    // Combinational
    assign parity_out = tmp6;
    assign tmp0 = {data_in[0]};
    assign tmp1 = {data_in[1]};
    assign tmp2 = tmp0 ^ tmp1;
    assign tmp3 = {data_in[2]};
    assign tmp4 = tmp2 ^ tmp3;
    assign tmp5 = {data_in[3]};
    assign tmp6 = tmp4 ^ tmp5;

endmodule

