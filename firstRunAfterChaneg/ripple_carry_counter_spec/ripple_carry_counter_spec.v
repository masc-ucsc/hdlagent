module ripple_carry_counter_spec(input [0:0] clock, input [0:0] reset, output [3:0] q);
  reg [3:0] count;

  assign q = count;

  always @(posedge clock or posedge reset) begin
    if (reset) begin
      count <= 4'b0000;
    end else begin
      count[0] <= ~count[0];
      count[1] <= count[1] ^ count[0];
      count[2] <= count[2] ^ (count[1] & count[0]);
      count[3] <= count[3] ^ (count[2] & count[1] & count[0]);
    end
  end
endmodule
