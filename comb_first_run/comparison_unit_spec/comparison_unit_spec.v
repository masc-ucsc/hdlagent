module comparison_unit_spec(
    input logic [WIDTH-1:0] in1,
    input logic [WIDTH-1:0] in2,
    input logic [3:0] control,
    output logic predicate
);
    always_comb begin
        case(control)
            4'b0000: predicate = (in1 == {WIDTH{1'b0}}); // in1 equal to zero
            4'b0001: predicate = (in1 != {WIDTH{1'b0}}); // in1 not equal to zero
            4'b0010: predicate = 1'b1;                   // constant true
            4'b0011: predicate = ($signed(in1) >= $signed(in2)); // signed greater than or equal
            4'b0100: predicate = ($signed(in1) < $signed(in2));  // signed less than
            4'b0101: predicate = (in1 >= in2);          // unsigned greater than or equal
            4'b0110: predicate = (in1 < in2);           // unsigned less than
            4'b0111: predicate = (in1 == in2);          // equal
            4'b1000: predicate = (in1 != in2);          // not equal
            default: predicate = 1'b0;                  // default case
        endcase
    end
endmodule
