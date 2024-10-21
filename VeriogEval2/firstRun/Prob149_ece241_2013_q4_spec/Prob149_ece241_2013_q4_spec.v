module TopModule(
    input clk,
    input reset,
    input [2:0] s,
    output reg fr2,
    output reg fr1,
    output reg fr0,
    output reg dfr
);

    reg [2:0] previous_level;

    always @(*) begin
        // Default output values
        fr2 = 0;
        fr1 = 0;
        fr0 = 0;
        dfr = 0;

        if (s[2]) begin
            // Above s[2]
            fr2 = 0;
            fr1 = 0;
            fr0 = 0;
            dfr = 0;
        end else if (s[1]) begin
            // Between s[2] and s[1]
            fr2 = 0;
            fr1 = 0;
            fr0 = 1;
            dfr = previous_level < 3'b010 ? 1 : 0;
        end else if (s[0]) begin
            // Between s[1] and s[0]
            fr2 = 0;
            fr1 = 1;
            fr0 = 1;
            dfr = previous_level < 3'b001 ? 1 : 0;
        end else begin
            // Below s[0]
            fr2 = 1;
            fr1 = 1;
            fr0 = 1;
            dfr = 1;
        end
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            previous_level <= 3'b000;
            fr2 <= 1;
            fr1 <= 1;
            fr0 <= 1;
            dfr <= 1;
        end else begin
            previous_level <= s;
        end
    end

endmodule
