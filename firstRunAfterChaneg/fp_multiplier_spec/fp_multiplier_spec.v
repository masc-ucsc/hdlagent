module fp_multiplier_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [31:0] input_a,
    input [0:0] input_a_stb,
    output reg [0:0] input_a_ack,
    input [31:0] input_b,
    input [0:0] input_b_stb,
    output reg [0:0] input_b_ack,
    output reg [31:0] output_z,
    output reg [0:0] output_z_stb,
    input [0:0] output_z_ack
);
    reg [7:0] exp_a, exp_b, exp_z;
    reg [23:0] mant_a, mant_b;
    reg [47:0] mant_z;
    reg sign_a, sign_b, sign_z;
    reg valid;
    
    always @(*) begin
        if (rst) begin
            input_a_ack = 0;
            input_b_ack = 0;
            output_z_stb = 0;
            output_z = 0;
        end else if (input_a_stb && input_b_stb && !valid) begin
            input_a_ack = 1;
            input_b_ack = 1;
            sign_a = input_a[31];
            sign_b = input_b[31];
            exp_a = input_a[30:23];
            exp_b = input_b[30:23];
            mant_a = {1'b1, input_a[22:0]};
            mant_b = {1'b1, input_b[22:0]};

            sign_z = sign_a ^ sign_b;
            exp_z = exp_a + exp_b - 127;
            mant_z = mant_a * mant_b;
            if (mant_z[47]) begin
                mant_z = mant_z >> 1;
                exp_z = exp_z + 1;
            end

            output_z = {sign_z, exp_z[7:0], mant_z[46:24]};
            output_z_stb = 1;
            valid = 1;
        end else if (output_z_ack && valid) begin
            output_z_stb = 0;
            input_a_ack = 0;
            input_b_ack = 0;
            valid = 0;
        end
    end
endmodule
