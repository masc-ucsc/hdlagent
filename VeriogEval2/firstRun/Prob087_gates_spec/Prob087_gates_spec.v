module Prob087_gates_spec(
    input [0:0] a,
    input [0:0] b,
    output [0:0] out_and,
    output [0:0] out_or,
    output [0:0] out_xor,
    output [0:0] out_nand,
    output [0:0] out_nor,
    output [0:0] out_xnor,
    output [0:0] out_anotb
);

assign out_and = a & b;      // AND gate
assign out_or = a | b;       // OR gate
assign out_xor = a ^ b;      // XOR gate
assign out_nand = ~(a & b);  // NAND gate
assign out_nor = ~(a | b);   // NOR gate
assign out_xnor = ~(a ^ b);  // XNOR gate
assign out_anotb = a & ~b;   // A AND NOT B

endmodule
