module TopModule(
    input [0:0] a,
    input [0:0] b,
    input [0:0] sel_b1,
    input [0:0] sel_b2,
    output [0:0] out_assign,
    output reg [0:0] out_always // output using reg type for always block
);

    // Using assign statement
    assign out_assign = (sel_b1 & sel_b2) ? b : a;

    // Using always block with procedural if statement
    always @(*) begin
        if (sel_b1 & sel_b2) begin
            out_always = b;
        end else begin
            out_always = a;
        end
    end

endmodule
