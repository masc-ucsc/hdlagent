module shift (
    input [0:0] clock,
     input [0:0] reset,
    input [0:0] data_i,
    output [4:0] data_o
);
  reg [4:0] shift_reg_r;
  always_ff @(posedge clock) begin
     shift_reg_r <= shift_reg_n;
  end
  reg [4:0] shift_reg_n;
  always_comb begin
  if (reset[0:0] == 1'b1) begin
    shift_reg_n = 0;
  end else begin
     shift_reg_n = {shift_reg_r[3:0], data_i[0:0]};
   end
  end
  assign data_o = shift_reg_r;
 endmodule

