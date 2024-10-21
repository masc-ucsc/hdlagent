module TopModule(input [2:0] y, input [0:0] w, output [0:0] Y1);
    wire [2:0] next_state;

    // Next-state logic for y[1]
    assign next_state[1] = (y == 3'b000 && w == 1'b1) || 
                           (y == 3'b001 && w == 1'b1) || 
                           (y == 3'b010 && w == 1'b1) || 
                           (y == 3'b011 && w == 1'b0) ||
                           (y == 3'b100 && w == 1'b1) ||
                           (y == 3'b101 && w == 1'b1);

    // Output logic
    assign Y1 = next_state[1];

endmodule
