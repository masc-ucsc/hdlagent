module mux2x1_behavioral (
    input a,
    input b,
    input select,
    output reg y
);
  always_comb begin
    case (select)
      0: y = a;
      1: y = b;
      default: y = 0;
    endcase
  end
endmodule



