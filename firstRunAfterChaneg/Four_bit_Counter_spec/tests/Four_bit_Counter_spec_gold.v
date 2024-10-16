module up_down_counter_8bit (
    input wire clock,
    input wire reset,
    input wire up_down,
    output wire [7:0] out_o
);

  reg [7:0] count;

  always @(posedge clock or posedge reset) begin
    if (reset) begin
      count <= 8'b00000000;
    end else if (up_down) begin
      count <= count + 1'b1;
    end else begin
      count <= count - 1'b1;
    end
  end

  assign out_o = count;
endmodule

