module SegmentCheck(
  input wire [3:0] seg_addr,
  input wire [7:0] SEGEXE_H,
  input wire [7:0] SEGEXE_L,
  output reg illegal_segment_address
);

  always @(*) begin
    if (seg_addr < 8) begin
      illegal_segment_address = SEGEXE_L[seg_addr] == 1'b0;
    end
    else if (seg_addr < 16) begin
      illegal_segment_address = SEGEXE_H[seg_addr-8] == 1'b0;
    end
    else begin
      illegal_segment_address = 1'b1;  // By default, indicate illegal if out of 16
    end
  end

endmodule

