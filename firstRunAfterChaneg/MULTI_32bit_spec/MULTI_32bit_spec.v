module MULTI_32bit_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [31:0] A,
    input [31:0] B,
    output reg [31:0] F
);
    reg [31:0] P1, P2, P3;
    reg [7:0] exp_A, exp_B, exp_sum;
    reg [23:0] mant_A, mant_B;
    reg [47:0] mant_prod;
    reg sign_prod;
    reg [23:0] mant_norm;
    reg [7:0] exp_res;
    reg [4:0] shift_amount;

    always @(*) begin
        // Stage 1: Sign Calculation
        sign_prod = A[31] ^ B[31];
        exp_A = A[30:23];
        exp_B = B[30:23];
        mant_A = {1'b1, A[22:0]};
        mant_B = {1'b1, B[22:0]};
        
        // Stage 2: Mantissa Multiplication and Exponent Adjustment
        mant_prod = mant_A * mant_B;
        exp_sum = exp_A + exp_B - 8'd127;
        
        P1 = {sign_prod, exp_sum, mant_prod[47:25]};
    end

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            P2 <= 32'b0;
        end else begin
            P2 <= P1;
        end
    end

    always @(*) begin
        // Stage 3: Normalization and Rounding
        casez (P2[24:23])
            2'b10, 2'b11: begin
                mant_norm = P2[23:1];
                exp_res = P2[30:23] + 1'b1;
            end
            2'b01: begin
                mant_norm = P2[23:0];
                exp_res = P2[30:23];
            end
            default: begin
                shift_amount = 0;
                while (!mant_norm[23]) begin
                    mant_norm = mant_norm << 1;
                    exp_res = exp_res - 1;
                    shift_amount = shift_amount + 1;
                end
                mant_norm = mant_norm[23:0];
            end
        endcase

        P3 = {P2[31], exp_res, mant_norm[22:0]};
    end

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            F <= 32'b0;
        end else begin
            F <= P3;
        end
    end
endmodule
