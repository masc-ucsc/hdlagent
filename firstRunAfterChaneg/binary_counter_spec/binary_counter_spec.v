module binary_counter_spec(input [0:0] clock, input [0:0] reset, input [0:0] enable, output reg [3:0] count);
    
    always @(posedge clock) begin
        if (reset) begin
            count <= 4'b0000; // reset counter to 0
        end else if (enable) begin
            count <= count + 1'b1; // increment counter
        end
    end

endmodule
