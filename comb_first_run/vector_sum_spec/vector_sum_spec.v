module vector_sum_spec(input [7:0] data, output [3:0] sum);
    integer i;
    reg [3:0] temp_sum;
    always @(*) begin
        temp_sum = 0;
        for (i = 0; i < 8; i = i + 1) begin
            temp_sum = temp_sum + data[i];
        end
    end
    assign sum = temp_sum;
endmodule
