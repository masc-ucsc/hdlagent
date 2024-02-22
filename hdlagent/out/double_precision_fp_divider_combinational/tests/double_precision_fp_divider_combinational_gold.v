module double_precision_fp_divider_combinational(
    input [63:0] input_a,
    input [63:0] input_b,
    output reg [63:0] output_z
);


wire sign_a = input_a[63];
wire [10:0] exponent_a = input_a[62:52];
wire [51:0] mantissa_a = {1'b1, input_a[51:0]};

wire sign_b = input_b[63];
wire [10:0] exponent_b = input_b[62:52];
wire [51:0] mantissa_b = {1'b1, input_b[51:0]};



wire a_is_nan_or_inf = exponent_a == 11'h7FF;
wire b_is_nan_or_inf = exponent_b == 11'h7FF;
wire a_is_zero = exponent_a == 0 && mantissa_a == 0;
wire b_is_zero = exponent_b == 0 && mantissa_b == 0;






wire [105:0] division_result = {mantissa_a, 54'b0} / mantissa_b;


wire result_sign = sign_a ^ sign_b;
wire [10:0] result_exponent = exponent_a - exponent_b + 1023;


always @(*) begin
    if (a_is_nan_or_inf || b_is_nan_or_inf) begin

        output_z = {1'b0, 11'h7FF, 52'h0};
    end else if (a_is_zero || b_is_zero) begin

        output_z = {result_sign, 11'h0, 52'h0};
    end else begin

        output_z = {result_sign, result_exponent, division_result[105:54]};
    end
end

endmodule






