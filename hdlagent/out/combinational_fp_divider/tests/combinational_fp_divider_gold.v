module combinational_fp_divider(
    input [31:0] input_a,
    input [31:0] input_b,
    output [31:0] output_z
);


    wire sign_a = input_a[31];
    wire [7:0] exp_a = input_a[30:23];
    wire [22:0] mant_a = input_a[22:0];

    wire sign_b = input_b[31];
    wire [7:0] exp_b = input_b[30:23];
    wire [22:0] mant_b = input_b[22:0];


    wire [23:0] norm_mant_a = {1'b1, mant_a};
    wire [23:0] norm_mant_b = {1'b1, mant_b};



    wire [47:0] div_result = {norm_mant_a, 24'b0} / norm_mant_b;


    wire result_sign = sign_a ^ sign_b;
    wire [8:0] exp_diff = {1'b0, exp_a} - {1'b0, exp_b};
    wire [7:0] result_exp = exp_diff[7:0] + 127;


    assign output_z = {result_sign, result_exp, div_result[46:24]};

endmodule






