module PCG32_spec(output [31:0] ouput_gen, input [0:0] clk);
    reg [63:0] state = 64'h4d595df4d0f33173; // initial state
    wire [63:0] next_state;
    wire [31:0] xorshifted, rot, output_value;
    
    // PCG update
    assign next_state = state * 64'd6364136223846793005 + 64'd1442695040888963407;
    
    // Output calculation
    assign xorshifted = ((state >> 18) ^ state) >> 27;
    assign rot = state >> 59;
    assign output_value = (xorshifted >> rot) | (xorshifted << ((~rot) + 1 | 6'd32));

    assign ouput_gen = output_value;
    
    always @(posedge clk) begin
        state <= next_state; // Update state on the clock's rising edge
    end
endmodule
