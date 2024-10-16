module fp_divider_spec(
    input [31:0] input_a,
    input [31:0] input_b,
    input [0:0] input_a_stb,
    input [0:0] input_b_stb,
    input [0:0] output_z_ack,
    input [0:0] clk,
    input [0:0] rst,
    output reg [31:0] output_z,
    output reg [0:0] output_z_stb,
    output reg [0:0] input_a_ack,
    output reg [0:0] input_b_ack
);

// State definition
typedef enum logic [3:0] {
    STATE_IDLE,
    STATE_GET_AB,
    STATE_UNPACK,
    STATE_SPECIAL_CASES,
    STATE_NORMALISE_AB,
    STATE_DIVIDE,
    STATE_NORMALISE_1,
    STATE_NORMALISE_2,
    STATE_ROUND,
    STATE_PACK,
    STATE_PUT_Z
} state_t;

// State register
state_t current_state, next_state;

// Internal signals
logic [31:0] a_mantissa, b_mantissa, z_mantissa;
logic [7:0] a_exponent, b_exponent, z_exponent;
logic a_sign, b_sign, z_sign;
logic guard, round, sticky;
logic [31:0] quotient;
integer i;

// State transition
always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
        current_state <= STATE_IDLE;
    end else begin
        current_state <= next_state;
    end
end

// State machine
always_comb begin
    // Default assignments
    next_state = current_state;
    output_z_stb = 0;
    input_a_ack = 0;
    input_b_ack = 0;

    case (current_state)
        STATE_IDLE: begin
            if (input_a_stb && input_b_stb) begin
                next_state = STATE_GET_AB;
            end
        end

        STATE_GET_AB: begin
            input_a_ack = 1;
            input_b_ack = 1;
            next_state = STATE_UNPACK;
        end

        STATE_UNPACK: begin
            a_sign = input_a[31];
            a_exponent = input_a[30:23];
            a_mantissa = {1'b1, input_a[22:0]};

            b_sign = input_b[31];
            b_exponent = input_b[30:23];
            b_mantissa = {1'b1, input_b[22:0]};

            if (a_exponent == 8'hFF || b_exponent == 8'hFF) begin
                next_state = STATE_SPECIAL_CASES;
            end else begin
                next_state = STATE_DIVIDE;
            end
        end

        STATE_SPECIAL_CASES: begin
            // Handle special cases like NaN or Infinity (pseudocode)
            // if (input_a is NaN or input_b is NaN) set output_z to NaN
            // if (input_b is 0) handle division by 0 case
            // if (input_a is infinity and input_b is not infinity) handle accordingly
            next_state = STATE_PACK;
        end

        STATE_DIVIDE: begin
            z_sign = a_sign ^ b_sign;

            // Adjustment to account for bias
            z_exponent = a_exponent - b_exponent + 8'd127;
    
            // Shift and subtract method to calculate quotient
            quotient = 0;
            for (i = 0; i < 24; i = i + 1) begin
                quotient = quotient << 1;
                a_mantissa = a_mantissa - b_mantissa;
                if (~a_mantissa[31]) begin
                    quotient = quotient | 1'b1;
                end else begin
                    a_mantissa = a_mantissa + b_mantissa;
                end
                a_mantissa = a_mantissa << 1;
            end
            z_mantissa = quotient[31:8];
            guard = quotient[7];
            round = quotient[6];
            sticky = |quotient[5:0];

            next_state = STATE_NORMALISE_1;
        end

        STATE_NORMALISE_1: begin
            if (z_mantissa[23] == 0 && z_exponent > 0) begin
                z_mantissa = z_mantissa << 1;
                z_exponent = z_exponent - 1;
            end
            next_state = STATE_NORMALISE_2;
        end

        STATE_NORMALISE_2: begin
            // Similar normalization
            next_state = STATE_ROUND;
        end

        STATE_ROUND: begin
            // Apply rounding (pseudocode)
            // if (guard and (round or sticky) or guard and not round and sticky) increment z_mantissa
            next_state = STATE_PACK;
        end

        STATE_PACK: begin
            if (z_exponent > 8'hFE) begin
                // overflow, set to infinity
                output_z = {z_sign, 8'hFF, 23'b0};
            end else if (z_exponent < 8'h01) begin
                // underflow, set to zero
                output_z = {z_sign, 8'h0, 23'b0};
            end else begin
                output_z = {z_sign, z_exponent, z_mantissa[22:0]};
            end
            next_state = STATE_PUT_Z;
        end

        STATE_PUT_Z: begin
            output_z_stb = 1;
            if (output_z_ack) begin
                next_state = STATE_IDLE;
            end
        end
    endcase
end

endmodule
