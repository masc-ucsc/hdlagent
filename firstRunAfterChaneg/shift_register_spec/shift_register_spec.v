module shift_register_spec(input [0:0] clock,
                           input [0:0] reset,
                           input [0:0] serial_in,
                           output reg [0:0] serial_out,
                           output reg [3:0] parallel_out);

  always @(negedge clock or posedge reset) begin
    if (reset) begin
      parallel_out <= 4'b0000; // Resetting the shift register
    end else begin
      parallel_out <= {parallel_out[2:0], serial_in}; // Shifting on the falling edge
    end
  end
  
  always @(parallel_out) begin
    serial_out <= parallel_out[3]; // Outputting the MSB as serial_out
  end

endmodule
