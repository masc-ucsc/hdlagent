module four_bit_sync_counter (
    input clock,
    input reset,
    output [3:0] out_o
);
  reg [3:0] temp;
  initial temp = 4'b0000;
  always @(posedge clock or posedge reset) begin
    if (reset) temp <= 4'b0000;
    else temp <= temp + 1;
  end
  assign out_o = temp;
endmodule

