module Four_bit_Counter_spec(input [0:0] clock, input [0:0] reset, output reg [3:0] count);

always @(posedge clock or posedge reset) begin
    if (reset) 
        count <= 4'b0000; // asynchronous reset
    else 
        count <= count + 1'b1; // increment on positive edge of clock
end

endmodule
