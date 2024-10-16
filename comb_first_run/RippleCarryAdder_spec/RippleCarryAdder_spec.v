module FullAdder(input a, input b, input ci, output sum, output co);
    assign {co, sum} = a + b + ci;
endmodule
module RippleCarryAdder_spec(input [3:0] a, input [3:0] b, output [4:0] sum);
    wire [3:0] carry; // Internal carry wires
    
    // First FullAdder, carry-in is 0
    FullAdder fa0(.a(a[0]), .b(b[0]), .ci(1'b0), .sum(sum[0]), .co(carry[0]));
    
    // Second FullAdder
    FullAdder fa1(.a(a[1]), .b(b[1]), .ci(carry[0]), .sum(sum[1]), .co(carry[1]));
    
    // Third FullAdder
    FullAdder fa2(.a(a[2]), .b(b[2]), .ci(carry[1]), .sum(sum[2]), .co(carry[2]));
    
    // Fourth FullAdder
    FullAdder fa3(.a(a[3]), .b(b[3]), .ci(carry[2]), .sum(sum[3]), .co(carry[3]));
    
    // Assign the final carry to sum[4]
    assign sum[4] = carry[3];
endmodule
