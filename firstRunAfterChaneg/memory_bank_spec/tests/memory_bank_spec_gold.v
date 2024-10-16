module binary_counter_4 (
    input clock,
    input reset,
    output reg [3:0] count
);
  always @(posedge clock) begin
    if (reset) count <= 4'b0000;
    else count <= count + 1;
  end
endmodule

