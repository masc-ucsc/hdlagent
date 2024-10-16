module up_down_counter (
    input clock,
    input reset,
    input up_down,
    input enable,
    output [3:0] count
);
  reg [3:0] counter;
  always @(posedge clock or negedge reset) begin
    if (!reset) counter <= 4'b0000;
    else if (enable) begin
      if (up_down) counter <= counter + 1;
      else counter <= counter - 1;
    end
  end
  assign count = counter;
endmodule

