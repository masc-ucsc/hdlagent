module mux2to1(
    input  [0:0] d0,
    input  [0:0] d1,
    input  [0:0] s,
    output  [0:0] reg y
);

always @(*) begin
    case(s)
        1'b0: y = d0;
        1'b1: y = d1;
    endcase
end

endmodule