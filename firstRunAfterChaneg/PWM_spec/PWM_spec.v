module PWM_spec(input [0:0] clk, input [0:0] rst, input [0:0] en, input [7:0] duty_cycle, output [0:0] pwm_out);

    wire [7:0] count;
    wire comp_out;

    // Instantiate the up counter
    UpCounter u_counter(
        .clk(clk),
        .rst(rst),
        .en(en),
        .count_out(count)
    );

    // Instantiate the comparator
    Comparator comp(
        .count(count),
        .duty_cycle(duty_cycle),
        .comp_out(comp_out)
    );

    // Instantiate the D flip flop
    DFF d_flip_flop(
        .clk(clk),
        .rst(rst),
        .d_in(comp_out),
        .q_out(pwm_out)
    );

endmodule
module UpCounter(input [0:0] clk, input [0:0] rst, input [0:0] en, output reg [7:0] count_out);
    always @(posedge clk or posedge rst) begin
        if (rst)
            count_out <= 8'b0;
        else if (en)
            count_out <= count_out + 1;
    end
endmodule
module Comparator(input [7:0] count, input [7:0] duty_cycle, output [0:0] comp_out);
    assign comp_out = (count < duty_cycle) ? 1'b1 : 1'b0;
endmodule
module DFF(input [0:0] clk, input [0:0] rst, input [0:0] d_in, output reg [0:0] q_out);
    always @(posedge clk or posedge rst) begin
        if (rst)
            q_out <= 1'b0;
        else
            q_out <= d_in;
    end
endmodule
