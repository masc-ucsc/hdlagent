module piso_shift_register (
    input clock,
    input reset,
    input load,
    input [3:0] data_in_parallel,
    output reg data_out_serial
);
  reg [3:0] shift_reg;
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      shift_reg <= 4'b0000;
    end else if (load) begin
  shift_reg <= data_in_parallel;
 end else begin
    shift_reg <= {shift_reg[2:0],1'b0};
    end
  end
  assign data_out_serial = shift_reg[3];
endmodule

