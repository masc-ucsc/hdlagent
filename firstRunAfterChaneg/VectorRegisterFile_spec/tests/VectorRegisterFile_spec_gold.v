module up_counter (
    input clock,
   input reset,
    output reg [1:0] count
);
  always @(posedge clock or posedge reset) begin
    if (reset) count = 2'b00;
    else count = count + 1;
  end
endmodule

