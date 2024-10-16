module edge_detection (
    input inp,
    output reg out1,
    output reg out2
);
  always @(posedge inp) out1 = 1'b1;
  always @(negedge inp) out2 = 1'b1;
endmodule

