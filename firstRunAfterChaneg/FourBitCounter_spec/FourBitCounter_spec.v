module FourBitCounter_spec(input [0:0] clock, input [0:0] reset, output reg [3:0] count);
  always @ (posedge clock or posedge reset) begin
    if (reset)
      count = 4'b0000; // Reset the counter to 0
    else
      count = count + 4'b0001; // Increment the counter
  end
endmodule
