module TopModule(input a, input b, output q);

  assign q = a & b; // q is high only when both a and b are high, based on the waveform

endmodule
