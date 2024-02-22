module count_ones (
    input [3:0] a,
    output reg [1:0] count
);
  always @(a) begin
    count = a[0] + a[1] + a[2] + a[3];
  end
endmodule


