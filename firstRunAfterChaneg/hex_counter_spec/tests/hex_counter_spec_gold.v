module PWM(
    input wire clk,
    input wire rst,
    input wire en,
    input wire [7:0] duty_cycle,
    output wire pwm_out
);
    wire cmp_out;
    wire [7:0] count;

    UpCounter u1(
        .clk(clk),
        .rst(rst),
        .en(en),
        .count(count)
    );

    Comparator c1(
        .duty_cycle(duty_cycle),
        .count(count),
        .cmp_out(cmp_out)
    );

    DFlipFlop d1(
        .clk(clk),
        .rst(rst),
        .d(cmp_out),
        .q(pwm_out)
    );

endmodule

module Comparator(
    input wire [7:0] duty_cycle,
    input wire [7:0] count,
    output wire cmp_out
);
    assign cmp_out = (count < duty_cycle) ? 1 : 0;
endmodule

module UpCounter(
    input wire clk,
    input wire rst,
    input wire en,
    output wire [7:0] count
);
    reg [7:0] count_reg;
    assign count = count_reg;

    always @(posedge clk or posedge rst) begin
        if (rst)
            count_reg <= 8'b0;
        else if (en)
            if (count_reg == 8'b11111111)
                count_reg <= 8'b0;
            else
                count_reg <= count_reg + 1;
    end
endmodule

module DFlipFlop(
    input wire clk,
    input wire rst,
    input wire d,
    output reg q
);
    always @(posedge clk or posedge rst) begin
        if (rst)
            q <= 0;
        else
            q <= d;
    end
endmodule

