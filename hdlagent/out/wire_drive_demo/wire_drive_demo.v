module wire_drive_demo(input [0:0] a, input [0:0] b, input [0:0] sel, output reg [0:0] w, output reg [0:0] w1, output reg [0:0] w2);

always @(*)
begin
    w1 = a & b;
    w2 = a | b;
    if(sel)
        w = w1;
    else
        w = w2;
end

endmodule