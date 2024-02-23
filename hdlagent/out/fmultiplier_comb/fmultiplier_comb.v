module fmultiplier_comb(
    input  [31:0] a,
    input  [31:0] b,
    output reg [31:0] z
); 
    // extract sections
    wire [31:23] a_exponent = a[30:23];
    wire [31:23] b_exponent = b[30:23];
    wire [22:0] a_mantissa = a[22:0];
    wire [22:0] b_mantissa = b[22:0];
    wire  a_sign = a[31];
    wire  b_sign = b[31];
    
    // add implicit '1' to mantissas of normalized numbers
    wire [23:0] a_mantissa_norm = a_exponent != 0 ? {1'b1, a_mantissa} : a_mantissa;
    wire [23:0] b_mantissa_norm = b_exponent != 0 ? {1'b1, b_mantissa} : b_mantissa;
    
    // multiply mantissas (24*24 bit multiplication results in 48 bits)
    wire [47:0] mantissa_product = a_mantissa_norm * b_mantissa_norm;
    
    // special cases: zero, infinity, NaN
    wire a_zero = a == 0;
    wire b_zero = b == 0;
    wire a_inf = a[30:0] == 31'b01111111100;
    wire b_inf = b[30:0] == 31'b01111111100;
    wire a_nan = a[30:0] > 31'b01111111100;
    wire b_nan = b[30:0] > 31'b01111111100;
    
    // output zeroinfinity, NaN
    assign z = a_zero || b_zero ? 32'b0 : a_inf || b_inf ? {a_sign ^ b_sign, 31'b01111111100} : a_nan || b_nan ? 32'b01111111111100000000000000000000 : z;
    
    // result exponent
    wire [7:0] exponent_sum8 = a_exponent + b_exponent;
    assign z[30:23] = exponent_sum8 - 127; // adjust for bias
    
    // normalize and round mantissa product
    assign z[22:0] = mantissa_product[47:25]; // select top 23 bits and implicitly round
    
    // result sign 
    assign z[31] = a_sign ^ b_sign;

endmodule