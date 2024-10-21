module TopModule(input [0:0] clk, input [7:0] in, output [7:0] pedge);
    reg [7:0] prev;
    
    always @(posedge clk) begin
        prev <= in;
    end 

    assign pedge = ~prev & in;
endmodule
