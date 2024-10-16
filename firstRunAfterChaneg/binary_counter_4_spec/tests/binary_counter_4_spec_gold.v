module moore_seq_detect (input x,
                         input clk,
                         input rst,
                         output reg z);
parameter s0 = 2'b00, s1 = 2'b01, s2 = 2'b10, s3 = 2'b11;

  reg[1:0] current_state, next_state;
    always @(posedge clk or negedge rst)
    begin
      if(!rst)
         current_state <= s0;
         else
         current_state <= next_state;
    end

   always@(*)
    begin
      case (current_state)
      s0 : begin
            if (x == 1)
                next_state = s1;
                else
                next_state = s0;
            end
      s1 : begin
            if (x == 1)
                next_state = s1;
                else
                next_state = s2;
            end
      s2 : begin
            if (x == 1)
                next_state = s3;
                else
                next_state = s0;
            end
      s3 : begin
            if (x == 1)
                next_state = s1;
                else
                next_state = s2;
            end
        default: next_state = s0;
      endcase
    end
    always@(*)
       if (current_state == s3)
           z = 1;
       else
           z = 0;
endmodule

