module TopModule(input [0:0] clk, input [0:0] load, input [255:0] data, output reg [255:0] q);
    
    reg [255:0] next_q;
    
    // Function to calculate the number of alive neighbors
    function [3:0] count_neighbors;
        input [3:0] row, col;
        integer i, j;
        reg [3:0] neighbors;
        begin
            neighbors = 0;
            for(i=-1; i<=1; i=i+1) begin
                for(j=-1; j<=1; j=j+1) begin
                    if (i != 0 || j != 0) begin
                        if (q[((row+i+16)%16)*16+((col+j+16)%16)] == 1'b1)
                            neighbors = neighbors + 1;
                    end
                end
            end
            count_neighbors = neighbors;
        end
    endfunction

    integer row, col;
    reg [3:0] neighbor_count;

    always @(*) begin
        for (row = 0; row < 16; row = row + 1) begin
            for (col = 0; col < 16; col = col + 1) begin
                neighbor_count = count_neighbors(row, col);
                case (neighbor_count)
                    4'd3: next_q[row*16 + col] = 1'b1;
                    4'd2: next_q[row*16 + col] = q[row*16 + col];
                    default: next_q[row*16 + col] = 1'b0;
                endcase
            end
        end
    end

    always @(posedge clk) begin
        if (load)
            q <= data;
        else
            q <= next_q;
    end

endmodule
