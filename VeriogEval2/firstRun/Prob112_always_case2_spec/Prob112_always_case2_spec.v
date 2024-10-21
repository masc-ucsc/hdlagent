module TopModule(input [3:0] in, output reg [1:0] pos);
    always @(*) begin
        casez (in)
            4'b1???: pos = 2'b11; // Priority for bit 3
            4'b01??: pos = 2'b10; // Priority for bit 2
            4'b001?: pos = 2'b01; // Priority for bit 1
            4'b0001: pos = 2'b00; // Priority for bit 0
            default: pos = 2'b00; // No bits are high
        endcase
    end
endmodule
