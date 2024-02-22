module double_precision_fp_divider_combinational(
  input  [63:0] input_a,
  input  [63:0] input_b,
  output reg [63:0] output_z
);
  // decompose the inputs
  wire [0:0] sa = input_a[63];                      // sign bit of input_a
  wire [0:0] sb = input_b[63];                      // sign bit of input_b
  wire [10:0] ea = input_a[62:52];                  // exponent of input_a
  wire [10:0] eb = input_b[62:52];                  // exponent of input_b
  wire [52:0] ma = {1'b1,input_a[51:0]};            // mantissa of input_a
  wire [52:0] mb = {1'b1,input_b[51:0]};            // mantissa of input_b

  // handle special cases
  wire NaN = (ea==11'b11111111111 && ma!=53'b0) || (eb==11'b11111111111 && mb!=53'b0); 
  wire zero = (ea==11'b00000000000 && ma==53'b0) || (eb==11'b00000000000 && mb==53'b0); 
  wire infinity = (ea==11'b11111111111 && ma==53'b0) || (eb==11'b11111111111 && mb==53'b0); 

  // division operation
  wire [0:0] sz = sa ^ sb;                          // sign of output_Z
  wire [10:0] ez = ea - eb + 11'b01111111111;       // exponent of output_Z
  wire [52:0] mz = ma / mb;                         // mantissa of output_Z

  // form the output data
  always @(*) begin
    if(NaN)
      output_z = 64'h7FF8000000000000;
    else if(zero)
      output_z = 64'h0000000000000000;
    else if(infinity)
      output_z = 64'h7FF0000000000000;
    else 
      output_z = {sz, ez, mz[51:0]};
  end
endmodule