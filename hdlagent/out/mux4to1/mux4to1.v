module mux4to1(
    output [0:0] out_o,
    input [0:0] in0,
    input [0:0] in1,
    input [0:0] in2,
    input [0:0] in3,
    input [1:0] sel
);

assign out_o = (sel[1]) ? (sel[0] ? in3 : in2) : (sel[0] ? in1 : in0);

endmodule
