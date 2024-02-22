module double_adder_combinational(
    input [63:0] input_a,
    input [63:0] input_b,
    output reg [63:0] output_z
);


wire sign_a = input_a[63];
wire [10:0] exp_a = input_a[62:52];
wire [51:0] mant_a = {1'b1, input_a[51:0]};

wire sign_b = input_b[63];
wire [10:0] exp_b = input_b[62:52];
wire [51:0] mant_b = {1'b1, input_b[51:0]};


wire is_a_nan = exp_a == 11'b11111111111 && |mant_a[50:0];
wire is_b_nan = exp_b == 11'b11111111111 && |mant_b[50:0];
wire is_a_inf = exp_a == 11'b11111111111 && ~|mant_a[50:0];
wire is_b_inf = exp_b == 11'b11111111111 && ~|mant_b[50:0];
wire is_a_zero = exp_a == 0 && mant_a == 0;
wire is_b_zero = exp_b == 0 && mant_b == 0;


wire [10:0] exp_diff = exp_a > exp_b ? exp_a - exp_b : exp_b - exp_a;
wire [51:0] aligned_mant_a = exp_a > exp_b ? mant_a : mant_a >> exp_diff;
wire [51:0] aligned_mant_b = exp_b > exp_a ? mant_b : mant_b >> exp_diff;


wire [52:0] sum_mantissa = sign_a == sign_b ? aligned_mant_a + aligned_mant_b : (aligned_mant_a > aligned_mant_b ? aligned_mant_a - aligned_mant_b : aligned_mant_b - aligned_mant_a);
wire result_sign = sign_a;


wire [52:0] normalized_mantissa = sum_mantissa[52] ? sum_mantissa >> 1 : sum_mantissa;
wire [10:0] adjusted_exp = sum_mantissa[52] ? (exp_a > exp_b ? exp_a + 1 : exp_b + 1) : (exp_a > exp_b ? exp_a : exp_b);


always @* begin
    if (is_a_nan || is_b_nan) begin
        output_z = {1'b1, 11'b11111111111, 1'b1, 50'd0};
    end else if (is_a_inf || is_b_inf) begin
        output_z = {result_sign, 11'b11111111111, 52'd0};
    end else if (is_a_zero && is_b_zero) begin
        output_z = {sign_a & sign_b, 11'd0, 52'd0};
    end else begin
        output_z = {result_sign, adjusted_exp, normalized_mantissa[51:0]};
    end
end

endmodule






