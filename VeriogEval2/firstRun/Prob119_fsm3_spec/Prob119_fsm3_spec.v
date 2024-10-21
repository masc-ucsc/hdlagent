module TopModule(input [0:0] clk, input [0:0] in, input [0:0] areset, output reg [0:0] out);

    // State encoding using reg type instead of enum to avoid casting issues
    reg [1:0] state, next_state;
    localparam [1:0] A = 2'd0, B = 2'd1, C = 2'd2, D = 2'd3;

    // State transition on clock edge or asynchronous reset
    always @(posedge clk or posedge areset) begin
        if (areset)
            state <= A;
        else
            state <= next_state;
    end

    // Next state logic and output logic
    always @(*) begin
        case (state)
            A: begin
                next_state = in ? B : A;
                out = 0;
            end
            B: begin
                next_state = in ? B : C;
                out = 0;
            end
            C: begin
                next_state = in ? D : A;
                out = 0;
            end
            D: begin
                next_state = in ? B : C;
                out = 1;
            end
            default: begin
                next_state = A;
                out = 0;
            end
        endcase
    end
endmodule
