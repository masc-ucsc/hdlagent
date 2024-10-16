module orn_spec(input [31:0] rs1, input [31:0] rs2, output [31:0] rd);
    assign rd = rs1 | ~rs2; // OR with inverted operand
endmodule
