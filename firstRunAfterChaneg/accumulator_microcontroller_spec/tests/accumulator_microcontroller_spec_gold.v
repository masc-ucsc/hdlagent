module binary_counter_6bit (
    input wire clock,
    input wire reset,
    output reg [5:0] counter
);
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      counter <= 6'b000000;
    end else begin
      if (counter == 6'b000110) begin
        counter <= 6'b000000;
      end else begin
        counter <= counter + 1;
      end
    end
  end
endmodule

