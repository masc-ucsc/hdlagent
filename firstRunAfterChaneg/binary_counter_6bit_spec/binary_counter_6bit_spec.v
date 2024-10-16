module binary_counter_6bit_spec(input [0:0] clock, input [0:0] reset, output reg [5:0] counter);

always @ (posedge clock) begin
    if (reset) 
        counter <= 6'b000000; // synchronous reset
    else if (counter == 6'b000110) 
        counter <= 6'b000000; // reset to 0 when counter reaches 6
    else
        counter <= counter + 1'b1; // increment counter
end

endmodule
