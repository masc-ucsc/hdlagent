module counter_n #(parameter WIDTH = 20)(input clk, output reg [WIDTH-1:0] count);
    always @(posedge clk) begin
        count <= count + 1;
    end
endmodule
module pmod_keypad_spec(input [0:0] clk, input [3:0] row, output reg [3:0] col, output reg [3:0] key);
    wire [19:0] key_counter;
    reg [1:0] col_select;
    
    counter_n #(.WIDTH(20)) cntr(.clk(clk), .count(key_counter));

    always @(posedge clk) begin
        // Select column based on counter's stable state
        case (key_counter[19:18])
            2'b00: col_select <= 2'b00; // Active column 0
            2'b01: col_select <= 2'b01; // Active column 1
            2'b10: col_select <= 2'b10; // Active column 2
            2'b11: col_select <= 2'b11; // Active column 3
        endcase
    end

    always @(*) begin
        // Set column based on col_select
        col = 4'b1111;
        col[col_select] = 1'b0;

        // Determine the key based on active column and row
        case (col_select)
            2'b00: // Column 0
                case (row)
                    4'b0001: key = 4'b0001; // Key 1
                    4'b0010: key = 4'b0100; // Key 4
                    4'b0100: key = 4'b0111; // Key 7
                    4'b1000: key = 4'b0000; // Key *
                    default: key = 4'b1111; // No key pressed
                endcase
            2'b01: // Column 1
                case (row)
                    4'b0001: key = 4'b0010; // Key 2
                    4'b0010: key = 4'b0101; // Key 5
                    4'b0100: key = 4'b1000; // Key 8
                    4'b1000: key = 4'b0000; // Key 0
                    default: key = 4'b1111; // No key pressed
                endcase
            2'b10: // Column 2
                case (row)
                    4'b0001: key = 4'b0011; // Key 3
                    4'b0010: key = 4'b0110; // Key 6
                    4'b0100: key = 4'b1001; // Key 9
                    4'b1000: key = 4'b1110; // Key #
                    default: key = 4'b1111; // No key pressed
                endcase
            2'b11: // Column 3
                case (row)
                    4'b0001: key = 4'b1010; // Key A
                    4'b0010: key = 4'b1011; // Key B
                    4'b0100: key = 4'b1100; // Key C
                    4'b1000: key = 4'b1101; // Key D
                    default: key = 4'b1111; // No key pressed
                endcase
        endcase
    end
endmodule
