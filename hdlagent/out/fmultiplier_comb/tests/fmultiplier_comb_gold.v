module fmultiplier_comb(a, b, z);

    input [31:0] a, b;
    output reg [31:0] z;


    wire [7:0] a_exp, b_exp;
    wire [23:0] a_mant, b_mant;
    wire a_sign, b_sign;

    assign a_sign = a[31];
    assign b_sign = b[31];
    assign a_exp = a[30:23];
    assign b_exp = b[30:23];
    assign a_mant = {1'b1, a[22:0]};
    assign b_mant = {1'b1, b[22:0]};


    wire a_is_zero, b_is_zero, a_is_inf, b_is_inf, a_is_nan, b_is_nan;
    assign a_is_zero = (a_exp == 0) && (a[22:0] == 0);
    assign b_is_zero = (b_exp == 0) && (b[22:0] == 0);
    assign a_is_inf = (a_exp == 255) && (a[22:0] == 0);
    assign b_is_inf = (b_exp == 255) && (b[22:0] == 0);
    assign a_is_nan = (a_exp == 255) && (a[22:0] != 0);
    assign b_is_nan = (b_exp == 255) && (b[22:0] != 0);


    wire [8:0] exp_sum;
    wire [7:0] z_exp;
    assign exp_sum = a_exp + b_exp - 127;
    assign z_exp = exp_sum[7:0];


    wire [47:0] mant_product;
    assign mant_product = a_mant * b_mant;


    wire [23:0] normalized_mant;
    wire need_shift;
    assign need_shift = mant_product[47];
    assign normalized_mant = need_shift ? mant_product[47:24] : mant_product[46:23];


    wire [23:0] rounded_mant;
    wire round_bit;
    assign round_bit = need_shift ? mant_product[23] : mant_product[22];
    assign rounded_mant = round_bit ? normalized_mant + 1 : normalized_mant;

    always @(*) begin
        if (a_is_nan || b_is_nan) begin
            z = {1'b0, 8'hFF, 1'b1, 22'b0};
        end else if (a_is_inf || b_is_inf) begin
            if (a_is_zero || b_is_zero) begin
                z = {1'b0, 8'hFF, 1'b1, 22'b0};
            end else begin
                z = {a_sign ^ b_sign, 8'hFF, 23'b0};
            end
        end else if (a_is_zero || b_is_zero) begin
            z = {a_sign ^ b_sign, 31'b0};
        end else begin

            z[31] = a_sign ^ b_sign;
            z[30:23] = z_exp;
            z[22:0] = rounded_mant[22:0];
        end
    end

endmodule



