module TopModule(input clk, input reset, output [9:0] q);
    reg [9:0] counter;

    always @(posedge clk) begin
        if (reset) 
            counter <= 10'b0000000000; // Reset counter to 0
        else if (counter == 10'd999)
            counter <= 10'b0000000000; // Reset counter when it reaches 999
        else 
            counter <= counter + 10'b0000000001; // Increment counter
    end

    assign q = counter; // Output the current counter value
endmodule
