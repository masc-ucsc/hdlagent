module param_difference_demo (
    output [3:0] o
);

  parameter reg [3:0] PARAM_VAL = 4'b1010;
  localparam reg [3:0] LocalparamVal = PARAM_VAL + 1;  // Renamed to CamelCase


  assign o = LocalparamVal;

endmodule


