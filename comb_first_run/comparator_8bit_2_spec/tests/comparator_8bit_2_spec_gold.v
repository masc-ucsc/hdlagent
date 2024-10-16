module bin_to_gray (
    input  [3:0] bin_in,
    output [3:0] gray_out
);
  assign gray_out = bin_in ^ (bin_in >> 1);
endmodule

