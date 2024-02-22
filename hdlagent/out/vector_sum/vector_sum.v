module vector_sum (
    input [7:0] data,
    output reg [3:0] sum
);

    always @* begin
        sum = 4'b0;
        integer i;
        for (i = 0; i < 8; i = i + 1) begin
            sum = sum + data[i];
        end
    end

endmodule