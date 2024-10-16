module float_to_int_spec(
    input [31:0] input_a,
    input [0:0] input_a_stb,
    input [0:0] output_z_ack,
    input [0:0] clk,
    input [0:0] rst,
    output reg [31:0] output_z,
    output reg [0:0] output_z_stb,
    output reg [0:0] input_a_ack
);

    // State Encoding
    localparam STATE_IDLE = 3'd0,
               STATE_UNPACK = 3'd1,
               STATE_SPECIAL_CASES = 3'd2,
               STATE_CONVERT = 3'd3,
               STATE_OUTPUT = 3'd4;

    reg [2:0] state, next_state;
    reg [31:0] mantissa;
    reg [7:0] exponent;
    reg sign;
    reg [31:0] result;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= STATE_IDLE;
            input_a_ack <= 1'b0;
            output_z_stb <= 1'b0;
            output_z <= 32'b0;
        end else begin
            state <= next_state;
        end
    end

    always @(*) begin
        next_state = state;
        input_a_ack = 1'b0;
        output_z_stb = 1'b0;

        case (state)
            STATE_IDLE: begin
                if (input_a_stb) begin
                    input_a_ack = 1'b1; // Acknowledge input
                    next_state = STATE_UNPACK;
                end
            end

            STATE_UNPACK: begin
                mantissa = {1'b1, input_a[22:0]};
                exponent = input_a[30:23] - 8'd127;
                sign = input_a[31];
                next_state = STATE_SPECIAL_CASES;
            end

            STATE_SPECIAL_CASES: begin
                if (exponent == 8'd255) begin
                    result = 32'h80000000; // Too large or NaN/Infinity
                    next_state = STATE_OUTPUT;
                end else if (exponent < 0) begin
                    result = 32'b0; // Too small (close to 0)
                    next_state = STATE_OUTPUT;
                end else begin
                    next_state = STATE_CONVERT;
                end
            end

            STATE_CONVERT: begin
                if (exponent > 31) begin
                    result = 32'h80000000; // Overflow
                end else begin
                    if (exponent <= 23)
                        result = mantissa >> (23 - exponent);
                    else
                        result = mantissa << (exponent - 23);

                    if (sign)
                        result = -result;
                end
                next_state = STATE_OUTPUT;
            end

            STATE_OUTPUT: begin
                output_z = result;
                output_z_stb = 1'b1; // Signal that output is valid
                if (output_z_ack) begin
                    next_state = STATE_IDLE;
                end
            end
        endcase
    end

endmodule
