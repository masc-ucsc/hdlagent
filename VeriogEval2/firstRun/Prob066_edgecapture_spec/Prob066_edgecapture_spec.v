module TopModule(input [0:0] clk, input [0:0] reset, input [31:0] in, output reg [31:0] out);

  reg [31:0] previous_in;

  always @(posedge clk) begin
    if (reset) begin
      out <= 32'b0;
      previous_in <= 32'b1; // Initialize to detect falling edge
    end else begin
      out <= out | (previous_in & ~in);
      previous_in <= in;
    end
  end

endmodule
