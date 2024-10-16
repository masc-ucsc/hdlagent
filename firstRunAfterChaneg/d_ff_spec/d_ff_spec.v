module d_ff_spec(input [0:0] clock, input [0:0] d, output [0:0] q);
    reg [0:0] q_reg;  // Create a reg type for storing the state of q
    assign q = q_reg; // Output the stored state
    
    always @(posedge clock) begin
        q_reg <= d; // On the rising edge of the clock, assign d to q_reg
    end
endmodule
