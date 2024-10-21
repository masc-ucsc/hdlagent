module TopModule(
    input [0:0] a,
    input [0:0] b,
    output [0:0] out_assign,
    output reg [0:0] out_alwaysblock  // Declare as reg for assignment in always block
);
    
    // AND gate using assign statement
    assign out_assign = a & b;

    // AND gate using always block
    always @(*) begin
        out_alwaysblock = a & b;
    end

endmodule
