module non_restoring_div_spec(
    input [0:0] clk,
    input [0:0] reset,
    input [63:0] Dividend,
    input [63:0] Divisor,
    output reg [63:0] Quotient,
    output reg [63:0] Remainder
);

    reg [63:0] a; // Accumulator for quotient building
    reg [63:0] p; // Partial remainder
    reg [5:0] count; // Loop counter

    always @(posedge clk or negedge reset) begin
        if (~reset) begin
            Quotient <= 64'b0;
            Remainder <= 64'b0;
            a <= Dividend;
            p <= 64'b0;
            count <= 6'd0;
        end else if (count < 6'd64) begin
            // Shift left (p, a)
            p = {p[62:0], a[63]};
            a = {a[62:0], 1'b0};

            // Add or Subtract based on the sign of p
            if (p[63] == 1'b0)
                p = p - Divisor;
            else
                p = p + Divisor;

            // Set the current quotient bit
            if (p[63] == 1'b0)
                a[0] = 1'b1;
            else
                a[0] = 1'b0;

            // Increment counter
            count = count + 1'b1;
        end else begin
            // Correction step
            if (p[63] == 1'b1)
                p = p + Divisor;

            // Assign outputs
            Quotient <= a;
            Remainder <= p;
        end
    end

endmodule
