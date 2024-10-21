module Prob139_2013_q2bfsm_spec(input [0:0] clk, input [0:0] resetn, input [0:0] x, input [0:0] y, output reg [0:0] f, output reg [0:0] g);

    reg [2:0] state;
    reg [1:0] y_counter;

    parameter A = 3'b000, B = 3'b001, C = 3'b010, D = 3'b011, E = 3'b100, F = 3'b101;

    always @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            state <= A;
            f <= 1'b0;
            g <= 1'b0;
            y_counter <= 2'b00;
        end else begin
            case (state)
                A: begin // Initial state
                    f <= 1'b1;
                    state <= B;
                end
                B: begin // Wait for 1->0->1 pattern on x
                    f <= 1'b0;
                    if (x) state <= C;
                end
                C: begin
                    if (!x) state <= D;
                end
                D: begin
                    if (x) state <= E;
                end
                E: begin // Set g = 1, check y for up to 2 cycles
                    g <= 1'b1;
                    y_counter <= 2'b00;
                    state <= F;
                end
                F: begin
                    if (y || y_counter == 2'b01) 
                        g <= 1'b1;
                    else if (y_counter == 2'b01) 
                        g <= 1'b0;

                    if (!y && y_counter != 2'b01)
                        y_counter <= y_counter + 1'b1;
                end
            endcase
        end
    end
endmodule
