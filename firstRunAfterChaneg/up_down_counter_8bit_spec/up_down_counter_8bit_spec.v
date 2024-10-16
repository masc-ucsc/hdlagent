module up_down_counter_8bit_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] up_down,
    output reg [7:0] out_o
);
    reg [7:0] next_out;
    
    always @(*) begin
        if (reset) begin
            next_out = 8'b0;  // Set counter to 0 on reset
        end else if (up_down) begin
            next_out = out_o + 8'b00000001;  // Increment when up_down is 1
        end else begin
            next_out = out_o - 8'b00000001;  // Decrement when up_down is 0
        end
    end
    
    always @(posedge clock or posedge reset) begin
        if (reset) begin
            out_o <= 8'b0;  // Reset counter
        end else begin
            out_o <= next_out;  // Update counter
        end
    end

endmodule
