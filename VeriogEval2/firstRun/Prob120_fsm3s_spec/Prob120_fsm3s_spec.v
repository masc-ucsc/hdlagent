module TopModule(input clk, input reset, input in, output reg out);

    // Define state encoding
    localparam A = 2'b00;
    localparam B = 2'b01;
    localparam C = 2'b10;
    localparam D = 2'b11;
    
    reg [1:0] current_state, next_state;

    // State transition logic
    always @(*) begin
        case (current_state)
            A: begin
                if (in == 0) next_state = A;
                else next_state = B;
                out = 0;
            end
            B: begin
                if (in == 0) next_state = C;
                else next_state = B;
                out = 0;
            end
            C: begin
                if (in == 0) next_state = A;
                else next_state = D;
                out = 0;
            end
            D: begin
                if (in == 0) next_state = C;
                else next_state = B;
                out = 1;
            end
            default: begin
                next_state = A;
                out = 0;
            end
        endcase
    end

    // State update logic with synchronous reset
    always @(posedge clk or posedge reset) begin
        if (reset)
            current_state <= A;
        else
            current_state <= next_state;
    end

endmodule
