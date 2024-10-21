module TopModule(
    input [0:0] x,
    input [2:0] y,
    output [0:0] Y0,
    output [0:0] z
);
    reg [2:0] Y;
    
    always @(*) begin
        case (y)
            3'b000: Y = (x == 0) ? 3'b000 : 3'b001;
            3'b001: Y = (x == 0) ? 3'b001 : 3'b100;
            3'b010: Y = (x == 0) ? 3'b010 : 3'b001;
            3'b011: Y = (x == 0) ? 3'b001 : 3'b010;
            3'b100: Y = (x == 0) ? 3'b011 : 3'b100;
            default: Y = 3'b000;
        endcase
    end

    assign Y0 = Y[0];  // Output logic
    assign z = (y == 3'b011 || y == 3'b100) ? 1'b1 : 1'b0;
    
endmodule
