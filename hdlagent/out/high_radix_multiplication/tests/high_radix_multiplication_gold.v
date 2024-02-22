module high_radix_multiplication(x, y, out_o);
    input [15:0] x, y;
    output [31:0] out_o;

    wire [15:0] inv_x = (~x) + 1'b1;
    wire [31:0] product[0:7];
    wire [31:0] sum[0:5];


    function [31:0] compute_product;
        input [15:0] x, inv_x;
        input [1:0] y_bits;
        begin
            case (y_bits)
                2'b00, 2'b11: compute_product = 32'b0;
                2'b01: compute_product = { {16{x[15]}}, x };
                2'b10: compute_product = { {16{inv_x[15]}}, inv_x };
                default: compute_product = 32'b0;
            endcase
        end
    endfunction

    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : gen_partial_products
            wire [1:0] y_bits = y[2*i+1:2*i];
            assign product[i] = compute_product(x, inv_x, y_bits) << (2*i);
        end
    endgenerate


    assign sum[0] = product[0] + product[1];
    assign sum[1] = product[2] + product[3];
    assign sum[2] = product[4] + product[5];
    assign sum[3] = product[6] + product[7];
    assign sum[4] = sum[0] + sum[1];
    assign sum[5] = sum[2] + sum[3];
    assign out_o = sum[4] + sum[5];

endmodule



