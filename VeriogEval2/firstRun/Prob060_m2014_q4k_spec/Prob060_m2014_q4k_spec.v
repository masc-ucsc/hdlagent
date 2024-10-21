module TopModule(input clk, input resetn, input in, output out);
    reg [3:0] shift_reg;

    always @(posedge clk) begin
        if (!resetn) 
            shift_reg <= 4'b0000; // Active low reset
        else 
            shift_reg <= {shift_reg[2:0], in}; // Shift left and insert input
    end
    
    assign out = shift_reg[3]; // Output the last bit of the shift register
endmodule
module Prob060_m2014_q4k_spec(input [0:0] clk, input [0:0] resetn, input [0:0] in, output [0:0] out);
    TopModule u1(.clk(clk), .resetn(resetn), .in(in), .out(out));
endmodule
