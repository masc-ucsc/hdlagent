module combinational_fp_divider
(
  input  [31:0] input_a,
  input  [31:0] input_b,
  output  [31:0] output_z
);

  wire   [22:0] mantissa_a = input_a[22:0];
  wire   [22:0] mantissa_b = input_b[22:0];
  wire           sign_a = input_a[31];
  wire           sign_b = input_b[31];
  wire   [7:0]   exponent_a = input_a[30:23] - 8'b01111111;
  wire   [7:0]   exponent_b = input_b[30:23] - 8'b01111111;

  wire           sign_z = sign_a ^ sign_b;
  
  reg    [46:0]  dividend = {1'b1, mantissa_a, 23'b0};
  reg    [23:0]  divisor = {1'b1, mantissa_b};

  wire   [46:0]  quotient = dividend / divisor;
  
  assign output_z[31] = sign_z;

  always @* begin
    if (divisor == 0) begin
      output_z[30:23] = 8'b11111111;  // Inf
      output_z[22:0] = 0;
    end else if (dividend == 0 || quotient[46:24] == 0) begin
      output_z[30:23] = 0;  // zero
      output_z[22:0] = 0;
    end else begin
      output_z[30:23] = exponent_a-exponent_b+127;
      output_z[22:0] = quotient[46:23];
    end
  end

endmodule