module TopModule(input clk, input reset, output [4:0] q);
    reg [4:0] lfsr;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            lfsr <= 5'b00001; // Active-high reset to 1
        end else begin
            lfsr[4] <= lfsr[0]; // Shift
            lfsr[3] <= lfsr[4] ^ lfsr[0]; // Tap at position 3 and 5
            lfsr[2] <= lfsr[3];
            lfsr[1] <= lfsr[2];
            lfsr[0] <= lfsr[1];
        end
    end

    assign q = lfsr;

endmodule
