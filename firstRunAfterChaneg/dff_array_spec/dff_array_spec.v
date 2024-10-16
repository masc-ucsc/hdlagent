module dff_array_spec(input [7:0] d, input [0:0] clock, output [7:0] q);

  genvar i;
  generate
    for (i = 0; i < 8; i = i + 1) begin : dff_loop
      dff dff_inst (
        .d(d[i]),
        .clock(clock),
        .q(q[i])
      );
    end
  endgenerate

endmodule
module dff(input d, input clock, output reg q);
  always @(posedge clock) begin
    q <= d;
  end
endmodule
