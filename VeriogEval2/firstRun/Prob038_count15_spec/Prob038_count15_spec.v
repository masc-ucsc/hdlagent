module TopModule(input clk, input reset, output [3:0] q);
    reg [3:0] counter;

    always @(posedge clk) begin
        if (reset)
            counter <= 4'b0000; // Synchronous reset to 0
        else
            counter <= counter + 1'b1; // Increment counter
    end

    assign q = counter; // Output the current counter value
endmodule
