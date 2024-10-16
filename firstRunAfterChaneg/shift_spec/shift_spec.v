module shift_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] data_i,
    output reg [4:0] data_o
);

always @(posedge clock) begin
    if (reset) begin
        data_o <= 5'b00000; // Reset to 0
    end else begin
        data_o <= {data_o[3:0], data_i}; // Shift left and insert data_i
    end
end

endmodule
