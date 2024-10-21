module TopModule(input clk, input w, input R, input E, input L, output reg Q);

    always @(posedge clk) begin
        if (L) 
            Q <= R; // Load operation
        else if (E) 
            Q <= w; // Shift operation
    end

endmodule
