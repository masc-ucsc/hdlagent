module Prob032_vector0_spec(
    input [2:0] vec,
    output [2:0] outv,
    output [0:0] o2,
    output [0:0] o1,
    output [0:0] o0
);
    // Assign the output vector to be the same as the input vector
    assign outv = vec;
    // Split the input vector into separate bits
    assign o2 = vec[2];
    assign o1 = vec[1];
    assign o0 = vec[0];
endmodule
