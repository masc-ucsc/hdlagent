module shift_register (
    input wire clock,
    input wire reset,
    input wire serial_in,
    output wire serial_out,
    output wire [3:0] parallel_out
);


  reg [3:0] register;


  assign serial_out   = register[0];


  assign parallel_out = register;


  always @(negedge clock or posedge reset) begin
    if (reset)

      register <= 4'b0000;
    else

      register <= {
        serial_in, register[3:1]
      };
  end

endmodule

