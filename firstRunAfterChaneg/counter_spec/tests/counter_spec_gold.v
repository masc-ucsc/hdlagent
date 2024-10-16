module non_blocking_swap (
    input clock,
    input [3:0] r1,
    input [3:0] r2,
    output reg [3:0] s1,
    output reg [3:0] s2
);
  always @(posedge clock) begin
    s1 <= r2;
    s2 <= r1;
  end
endmodule

