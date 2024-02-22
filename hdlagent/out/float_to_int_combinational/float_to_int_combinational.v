module float_to_int_combinational (
    input  [31:0] input_a,
    output reg [31:0] output_z
);
    wire [7:0]    exponent = input_a[30:23];
    wire [22:0]   mantissa = input_a[22:0];
    wire          sign     = input_a[31];
    wire [31:0]   result;
    wire          is_zero_denormal = exponent == 8'b0;

    assign result = is_zero_denormal ? 32'd0 :
                    {1'b1, mantissa} << (exponent - 8'd127);

    wire is_overflow = (exponent-127) > 30;

    assign output_z = is_zero_denormal ? 32'd0 :
                      is_overflow ? (sign ? 32'h80000000 : 32'h7fffffff) :
                      sign ? -result : result;
endmodule