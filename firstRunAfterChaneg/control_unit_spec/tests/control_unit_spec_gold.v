module johnson_counter (
    input clock,
    input reset,
    output reg [3:0] q
);
  reg [3:0] shift_reg;
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      shift_reg <= 4'b0001;
    end else begin
      shift_reg <= {shift_reg[0], shift_reg[3:1]};
    end
  end
  assign q = shift_reg;
endmodule

