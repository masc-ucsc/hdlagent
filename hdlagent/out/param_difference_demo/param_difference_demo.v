module param_difference_demo (
    output reg [3:0] o
);

parameter value = 10;
localparam local_value = value + 1;

assign o = local_value;

endmodule