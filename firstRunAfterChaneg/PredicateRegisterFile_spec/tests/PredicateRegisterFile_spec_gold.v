module binary_counter (
    input wire clock,
    input wire reset,
    input wire enable,
    output reg [3:0] count
);

  always @(posedge clock) begin
    if (reset) count <= 4'b0000;
    else if (enable) count <= count + 1'b1;
  end

endmodule

