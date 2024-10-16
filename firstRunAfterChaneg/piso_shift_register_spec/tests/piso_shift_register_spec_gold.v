module dff_array (
    input [7:0] d,
    input clock,
    output [7:0] q
);

  genvar i;

  generate
    for (i = 0; i < 8; i = i + 1) begin : gen_DFF_INST

      always @(posedge clock) q[i] <= d[i];

    end
  endgenerate

endmodule

