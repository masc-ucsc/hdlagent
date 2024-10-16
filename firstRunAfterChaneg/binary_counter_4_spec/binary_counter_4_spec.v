module binary_counter_4_spec(input [0:0] clock, input [0:0] reset, output [3:0] count);
    reg [3:0] count_reg;
    
    always @(*) begin
        if (reset) begin // synchronous, positive edge reset
            count_reg = 4'b0000;
        end else if (clock) begin // increment on clock edge
            count_reg = count_reg + 1;
        end
    end

    assign count = count_reg;
endmodule
