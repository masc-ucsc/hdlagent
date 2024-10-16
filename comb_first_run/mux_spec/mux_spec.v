module mux_spec(input [1:0] sel, input [7:0] i0, input [7:0] i1, input [7:0] i2, output [7:0] out_o);
    assign out_o = (sel == 2'b00) ? i0 :
                   (sel == 2'b01) ? i1 :
                   (sel == 2'b10) ? i2 : 8'b00000000;
endmodule
