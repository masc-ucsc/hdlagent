module universal_shift_register (
    input clock,
    input reset,
    input shift_dir,
    input shift_mode,
    input [3:0] data_in,
    input data_in_serial,
    output reg [3:0] q
);
  reg [3:0] shift_reg;
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      shift_reg <= 4'b0000;
    end else begin
      if (shift_mode) begin
        shift_reg <= data_in;
      end else begin
        if (shift_dir) begin
          shift_reg <= {data_in_serial, shift_reg[3:1]};
        end else begin
          shift_reg <= {shift_reg[2:0], data_in_serial};
        end
      end
    end
  end
  assign q = shift_reg;
endmodule

