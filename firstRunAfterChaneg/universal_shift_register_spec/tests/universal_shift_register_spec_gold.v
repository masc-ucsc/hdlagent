module ripple_carry_counter (
    input  wire       clock,
    input  wire       reset,
    output reg  [3:0] q
);

  reg q0, q1, q2, q3;
  always @(posedge clock) begin
    if (reset) begin
      q0 <= 1'b0;
      q1 <= 1'b0;
      q2 <= 1'b0;
      q3 <= 1'b0;
    end else begin
      q0 <= ~q0;
      if (q0)
         begin
        q1 <= ~q1;
        if (q1) begin
          q2 <= ~q2;
          if (q2) q3 <= ~q3;
        end
      end
    end
  end

  assign q[3:0] = {q3, q2, q1, q0};
endmodule

