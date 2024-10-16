module johnson_counter_spec(input [0:0] clock, input [0:0] reset, output reg [3:0] q);
    always @ (posedge clock or posedge reset) begin
        if (reset)
            q <= 4'b0001; // Reset state
        else
            q <= {q[0], q[3:1]}; // Right shift with feedback
    end
endmodule
