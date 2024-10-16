module dual_counters (
    input clock,
    input reset,
    output reg [3:0] count1,
    output reg [3:0] count2
);
  always @(posedge clock) begin
 if (reset) begin
count1 <= 'b0; end
else begin count1 <= count1 + 1'b1;
end end
  always @(negedge clock) begin
if (reset) begin
 count2 <= 'b0; end
 else begin count2 <= count2 - 1'b1;
end end
endmodule

