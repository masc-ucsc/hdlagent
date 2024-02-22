module param_demo (
    output reg [3:0] o
);

  parameter reg [3:0] FixedVal = 4'b1001;
  localparam reg [3:0] ModifiedVal = FixedVal + 1;

  initial begin
    o = ModifiedVal;
  end

endmodule


