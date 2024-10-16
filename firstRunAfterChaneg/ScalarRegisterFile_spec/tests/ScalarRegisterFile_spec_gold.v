module hex_counter (
    input wire clock,
     input wire reset,
     output wire [3:0] q
);
  reg [3:0] tmp;
  always @(posedge clock or posedge reset) begin
    if (reset) tmp <= 0;
    else if (tmp == 'b1111) tmp <= 'b0;
    else tmp <= tmp + 1'b1;
   end
  assign q = tmp;
endmodule

