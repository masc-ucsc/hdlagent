module double_adder_combinational(
    input  [63:0] input_a,
    input  [63:0] input_b,
    output reg [63:0] output_z
);
    // Decode inputs
    wire [0:0]   sign_a = input_a[63];
    wire [10:0]  exp_a  = input_a[62:52];
    wire [51:0]  man_a  = {1'b1,input_a[51:0]};
    
    wire [0:0]   sign_b = input_b[63];
    wire [10:0]  exp_b  = input_b[62:52];
    wire [51:0]  man_b  = {1'b1,input_b[51:0]};
    
    wire [12:0]  exp_diff = exp_a - exp_b;
    
    // Align mantissas based on exponent difference
    wire [52:0]  man_shift_a = man_a >> exp_diff;
    wire [52:0]  man_shift_b = man_b;
    
    // Perform addition or subtraction based on signs
    wire [52:0]  man_sum;
    assign man_sum = sign_a ? (man_shift_b - man_shift_a) : (man_shift_a + man_shift_b);
    
    // Normalize result
    wire [0:0]   sign_z = sign_a; // Assume same as input_a's sign for simplicity
    wire [10:0]  exp_z;
    wire [51:0]  man_z;
    
    always @* begin
        if (man_sum[52]) begin
            // Needs normalization
            man_z = man_sum[51:1];
            exp_z = exp_a + 1'b1;
        end else begin
            // Already normalized
            man_z = man_sum[52:2];
            exp_z = exp_a;
        end
    end
    
    // Construct output
    assign output_z = {sign_z, exp_z, man_z[50:0]};
    
endmodule