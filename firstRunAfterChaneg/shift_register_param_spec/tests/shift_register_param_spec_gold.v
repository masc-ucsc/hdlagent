`timescale 1ns / 1ps
 module pmod_keypad(
    input clk,
    input [3:0] row,
    output reg [3:0] col,
    output reg [3:0] key
    );


    localparam BITS = 20;


    localparam ONE_MS_TICKS = 100000000 / 1000;


    localparam SETTLE_TIME = 100000000 / 1000000;

    wire [BITS - 1 : 0] key_counter;
    reg rst = 1'b0;


    counter_n #(.BITS(BITS)) counter(
        .clk(clk),
        .rst(rst),
        .q(key_counter)
    );


    always @ (posedge clk)
    begin
        case (key_counter)
            0:
                rst <= 1'b0;

            ONE_MS_TICKS:
                col <= 4'b0111;

            ONE_MS_TICKS + SETTLE_TIME:
            begin
                case (row)
                    4'b0111:
                        key <= 4'b0001;
                    4'b1011:
                        key <= 4'b0100;
                    4'b1101:
                        key <= 4'b0111;
                    4'b1110:
                        key <= 4'b0000;
                endcase
            end

            2 * ONE_MS_TICKS:
                col <= 4'b1011;

            2 * ONE_MS_TICKS + SETTLE_TIME:
            begin
                case (row)
                    4'b0111:
                        key <= 4'b0010;
                    4'b1011:
                        key <= 4'b0101;
                    4'b1101:
                        key <= 4'b1000;
                    4'b1110:
                        key <= 4'b1111;
                endcase
            end


            3 * ONE_MS_TICKS:
                col <= 4'b1101;

            3 * ONE_MS_TICKS + SETTLE_TIME:
            begin
                case (row)
                    4'b0111:
                        key <= 4'b0011;
                    4'b1011:
                        key <= 4'b0110;
                    4'b1101:
                        key <= 4'b1001;
                    4'b1110:
                        key <= 4'b1110;
                endcase
            end


            4 * ONE_MS_TICKS:
                col <= 4'b1110;

            4 * ONE_MS_TICKS + SETTLE_TIME:
            begin
                case (row)
                    4'b0111:
                        key <= 4'b1010;
                    4'b1011:
                        key <= 4'b1011;
                    4'b1101:
                        key <= 4'b1100;
                    4'b1110:
                        key <= 4'b1101;
                endcase


                rst <= 1'b1;
            end
        endcase
    end

endmodule

module counter_n
    # (BITS = 4)
    (
    input clk,
    input rst,
    output tick,
    output [BITS - 1 : 0] q
    );


    reg [BITS - 1 : 0] rCounter = 0;


    always @ (posedge clk, posedge rst)
        if (rst)
            rCounter <= 0;
        else
            rCounter <= rCounter + 1;


    assign q = rCounter;


    assign tick = (rCounter == 2 ** BITS - 1) ? 1'b1 : 1'b0;

endmodule

