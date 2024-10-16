module vector_sum (
    input [7:0] data,
    output reg [3:0] sum
);
  integer i;
  always @(data) begin
    sum = 0;
    for (i = 0; i < 8; i = i + 1) sum = sum + data[i];
  end
endmodule

