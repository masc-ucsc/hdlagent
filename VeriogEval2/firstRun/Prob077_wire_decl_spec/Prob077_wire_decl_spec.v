module TopModule(input a, input b, input c, input d, output out, output out_n);

  // Intermediate wires
  wire temp_and1, temp_and2;

  // First layer of AND gates
  assign temp_and1 = a & b;
  assign temp_and2 = c & d;
  
  // Second layer OR gate
  assign out = temp_and1 | temp_and2;

  // Inverted output
  assign out_n = ~out;

endmodule
