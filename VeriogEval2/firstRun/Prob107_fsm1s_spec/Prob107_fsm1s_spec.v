module TopModule(input [0:0] clk, input [0:0] in, input [0:0] reset, output [0:0] out);
  
  reg [0:0] state, next_state;
  parameter A = 1'b0, B = 1'b1;

  // State transition logic
  always @(state, in) begin
    case (state)
      B: next_state = (in == 1'b0) ? A : B;
      A: next_state = (in == 1'b0) ? B : A;
      default: next_state = B;
    endcase
  end

  // State register
  always @(posedge clk) begin
    if (reset == 1'b1)
      state <= B;
    else
      state <= next_state;
  end
  
  // Output logic
  assign out = (state == B) ? 1'b1 : 1'b0;

endmodule
