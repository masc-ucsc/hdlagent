module moore_seq_detect_spec(input [0:0] x, input [0:0] clk, input [0:0] rst, output [0:0] z);
  // State encoding
  parameter s0 = 2'b00, s1 = 2'b01, s2 = 2'b10, s3 = 2'b11;
  
  reg [1:0] current_state, next_state;
  reg z_reg;
  
  // State register
  always @(posedge clk or negedge rst) begin
    if (!rst)
      current_state <= s0; // Reset to initial state
    else
      current_state <= next_state;
  end

  // Next state logic
  always @(*) begin
    case (current_state)
      s0: next_state = (x == 1'b1) ? s1 : s0;
      s1: next_state = (x == 1'b0) ? s2 : s1;
      s2: next_state = (x == 1'b1) ? s3 : s0;
      s3: next_state = (x == 1'b0) ? s2 : s1;
      default: next_state = s0;
    endcase
  end

  // Output logic
  always @(*) begin
    z_reg = (current_state == s3) ? 1'b1 : 1'b0;
  end

  assign z = z_reg;
endmodule
