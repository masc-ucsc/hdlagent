module mux2to1 (
    input d0,
    input d1,
    input s,
    output reg y
);

  always_comb begin
    case (s)
      0: y = d0;
      1: y = d1;
      default: y = 0;
    endcase
  end

endmodule



