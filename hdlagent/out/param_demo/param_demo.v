module param_demo (
    output reg [3:0] o
);
  
  parameter VALUE = 9;
  localparam NEXT_VALUE = VALUE + 1;
  
  always @* begin
    o = NEXT_VALUE;
  end
  
endmodule