module TopModule(input [0:0] clk, input [0:0] load, input [511:0] data, output reg [511:0] q);
    wire [511:0] next_state;
    
    // Compute the next state for each cell
    generate
        genvar i;
        for (i = 0; i < 512; i = i + 1) begin : rule110_logic
            wire left = (i == 0) ? 1'b0 : q[i-1];
            wire center = q[i];
            wire right = (i == 511) ? 1'b0 : q[i+1];
            
            assign next_state[i] = (left & center & ~right) | (left & ~center) | (~left & center & right);
        end
    endgenerate

    // On clock edge, load data or update state
    always @(posedge clk) begin
        if (load) begin
            q <= data;
        end else begin
            q <= next_state;
        end
    end
endmodule
