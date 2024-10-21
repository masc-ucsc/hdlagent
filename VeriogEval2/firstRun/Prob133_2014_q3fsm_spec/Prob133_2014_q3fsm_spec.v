module Prob133_2014_q3fsm_spec(
    input [0:0] clk,
    input [0:0] reset,
    input [0:0] s,
    input [0:0] w,
    output reg [0:0] z
);

    reg [2:0] state;
    reg [1:0] count;

    // State encoding
    localparam A = 3'b000;
    localparam B = 3'b001;
    localparam C = 3'b010;
    localparam D = 3'b011;
    localparam E = 3'b100;
    localparam F = 3'b101;

    always @(posedge clk) begin
        if (reset) begin
            state <= A;
            count <= 2'b00;
            z <= 1'b0;
        end else begin
            case (state)
                A: begin
                    z <= 1'b0;
                    if (s) state <= B;
                end

                B: begin
                    z <= 1'b0;
                    if (w) count <= count + 1;
                    state <= C;
                end

                C: begin
                    if (w) count <= count + 1;
                    state <= D;
                end

                D: begin
                    if (w) count <= count + 1;
                    if (count == 2'b01) z <= 1'b1;
                    else z <= 1'b0;
                    count <= 2'b00;
                    state <= B;
                end

                default: begin
                    state <= A;  // default to reset state
                    count <= 2'b00;
                    z <= 1'b0;
                end
            endcase
        end
    end

endmodule
