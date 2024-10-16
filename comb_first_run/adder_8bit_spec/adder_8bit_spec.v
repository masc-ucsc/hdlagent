module adder_4bit(input [3:0] a, input [3:0] b, input [0:0] cin, output [3:0] sum, output [0:0] cout);
    wire [4:0] temp_sum;
    assign temp_sum = a + b + cin;
    assign sum = temp_sum[3:0];
    assign cout = temp_sum[4];
endmodule
module adder_8bit_spec(input [7:0] a, input [7:0] b, input [0:0] cin, output [7:0] sum, output [0:0] cout);
    wire [0:0] cout_lsb;

    // Lower 4 bits
    adder_4bit adder_lsb (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(cin),
        .sum(sum[3:0]),
        .cout(cout_lsb)
    );

    // Upper 4 bits
    adder_4bit adder_msb (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(cout_lsb),
        .sum(sum[7:4]),
        .cout(cout)
    );
endmodule
