module float_to_int_combinational(
    input [31:0] input_a,
    output reg [31:0] output_z
);


wire sign = input_a[31];
wire [7:0] exponent = input_a[30:23];
wire [22:0] mantissa = input_a[22:0];


wire [8:0] actual_exponent = exponent - 8'd127;


wire [23:0] normalized_mantissa = |exponent ? {1'b1, mantissa} : {1'b0, mantissa};


wire [8:0] shift_amount = 9'd23 - actual_exponent;


wire is_zero_or_denormalized = (exponent == 0);
wire is_overflow = (actual_exponent >= 9'd31);


wire [31:0] shifted_mantissa = normalized_mantissa >> shift_amount;


always @(*) begin
    if (is_zero_or_denormalized) begin

        output_z = 32'd0;
    end else if (is_overflow) begin

        output_z = sign ? 32'h80000000 : 32'h7FFFFFFF;
    end else begin

        output_z = sign ? -shifted_mantissa : shifted_mantissa;
    end
end

endmodule






