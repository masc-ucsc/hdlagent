module high_radix_multiplication(input  [15:0] x,input  [15:0] y,output  [31:0] out_o);
  wire [15:0] inv_x = ~x + 16'b1; // 2's complement of x
  reg [31:0] products0, products1, products2, products3, products4, products5, products6, products7;
  wire [31:0] sums0, sums1, sums2, sums3;

      always @*
        case (y[0 +: 2])
          2'b00, 2'b11: products0 = 32'b0;
          2'b01: products0 = {16'b0, x} << 0;
          2'b10: products0 = {16'b0, inv_x} << 0;
        endcase

      always @*
        case (y[2 +: 2])
          2'b00, 2'b11: products1 = 32'b0;
          2'b01: products1 = {16'b0, x} << 2;
          2'b10: products1 = {16'b0, inv_x} << 2;
        endcase

      always @*
        case (y[4 +: 2])
          2'b00, 2'b11: products2 = 32'b0;
          2'b01: products2 = {16'b0, x} << 4;
          2'b10: products2 = {16'b0, inv_x} << 4;
        endcase

      always @*
        case (y[6 +: 2])
          2'b00, 2'b11: products3 = 32'b0;
          2'b01: products3 = {16'b0, x} << 6;
          2'b10: products3 = {16'b0, inv_x} << 6;
        endcase

      always @*
        case (y[8 +: 2])
          2'b00, 2'b11: products4 = 32'b0;
          2'b01: products4 = {16'b0, x} << 8;
          2'b10: products4 = {16'b0, inv_x} << 8;
        endcase

      always @*
        case (y[10 +: 2])
          2'b00, 2'b11: products5 = 32'b0;
          2'b01: products5 = {16'b0, x} << 10;
          2'b10: products5 = {16'b0, inv_x} << 10;
        endcase

      always @*
        case (y[12 +: 2])
          2'b00, 2'b11: products6 = 32'b0;
          2'b01: products6 = {16'b0, x} << 12;
          2'b10: products6 = {16'b0, inv_x} << 12;
        endcase

      always @*
        case (y[14 +: 2])
          2'b00, 2'b11: products7 = 32'b0;
          2'b01: products7 = {16'b0, x} << 14;
          2'b10: products7 = {16'b0, inv_x} << 14;
        endcase

  assign sums0 = products0 + products1;
  assign sums1 = products2 + products3;
  assign sums2 = products4 + products5;
  assign sums3 = products6 + products7;

  assign out_o = sums0 + sums1 + sums2 + sums3;

endmodule