module concurrent_toggles_spec(input [0:0] clock, input [0:0] reset, output reg [0:0] a, output reg [0:0] b);
    
    always @(posedge clock or posedge reset)
    begin
        if (reset)
            a <= 0;
        else
            a <= ~a;
    end

    always @(posedge clock or posedge reset)
    begin
        if (reset)
            b <= 0;
        else
            b <= ~b;
    end

endmodule
