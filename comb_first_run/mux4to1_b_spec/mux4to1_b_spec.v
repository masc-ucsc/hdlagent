module mux4to1_b_spec(input [3:0] a, input [1:0] s, output [0:0] y);
    assign y = (s == 2'b00) ? a[0] :
               (s == 2'b01) ? a[1] :
               (s == 2'b10) ? a[2] :
               a[3];
endmodule
