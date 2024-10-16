module Four_bit_Counter (
    input wire clock,
    input wire reset,
    output reg [3:0] count
);


  always @(posedge clock)
    if (!reset)
      count <= count + 1;
 else count <= 'b0;
endmodule

