module PCG32(output [31:0] ouput_gen, input [0:0] clk);
    reg [63:0] state;
    reg [31:0] rand_num;

    // LCG parameters
    localparam [63:0] multiplier = 64'h5851f42d4c957f2d;
    localparam [63:0] increment  = 64'h14057b7ef767814f;

    // Update state and generate random number
    always @(posedge clk) begin
        // Linear Congruential Generator (LCG) step
        state <= state * multiplier + increment;

        // PCG output permutation
        rand_num <= ((state >> ((state >> 59) + 5)) ^ state) >> 18;
    end

    assign ouput_gen = rand_num;
endmodule
