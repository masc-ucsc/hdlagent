module comparison_unit #(parameter WIDTH = 32)(
    input logic [WIDTH-1:0] in1,
    input logic [WIDTH-1:0] in2,
    input logic [3:0] control,
    output logic predicate
);

always_comb begin
    case (control)
        4'b0000: predicate = (in1 == 0);         4'b0001: predicate = (in1 != 0);  4'b0010: predicate = 1;       4'b0011: predicate = ($signed(in1) >= $signed(in2));        4'b0100: predicate = ($signed(in1) < $signed(in2));      4'b0101: predicate = (in1 >= in2);     4'b0110: predicate = (in1 < in2);   4'b0111: predicate = (in1 == in2);  4'b1000: predicate = (in1 != in2);   default: predicate = 0;    endcase
end

endmodule

