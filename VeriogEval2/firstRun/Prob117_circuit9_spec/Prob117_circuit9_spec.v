module TopModule(input clk, input a, output reg [2:0] q);

    always @(posedge clk) begin
        if (a == 1) begin
            q <= 4;
        end else begin
            if (q == 0)
                q <= 1;
            else if(q == 1)
                q <= 2;
            else if(q == 2)
                q <= 4;
            else if(q == 4)
                q <= 5;
            else if(q == 5)
                q <= 6;
            else if(q == 6)
                q <= 0;
        end
    end
endmodule
