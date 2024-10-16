module dual_counters_spec(input [0:0] clock, input [0:0] reset, output reg [3:0] count1, output reg [3:0] count2);

  // Process for incrementing count1 on rising edge
  always @(posedge clock) begin
    if (reset)
      count1 <= 4'b0000;
    else
      count1 <= count1 + 1;
  end

  // Process for decrementing count2 on falling edge
  always @(negedge clock) begin
    if (reset)
      count2 <= 4'b0000;
    else
      count2 <= count2 - 1;
  end

endmodule
