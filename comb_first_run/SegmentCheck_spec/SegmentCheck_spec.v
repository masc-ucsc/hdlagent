module SegmentCheck_spec(
    input [3:0] seg_addr,
    input [7:0] SEGEXE_H,
    input [7:0] SEGEXE_L,
    output [0:0] illegal_segment_address
    );
   
    wire [15:0] SEGEXE;
   
    // Combine high and low 8 bits into one 16-bit value
    assign SEGEXE = {SEGEXE_H, SEGEXE_L};
   
    // Check if the segment address is illegal
    assign illegal_segment_address = ~SEGEXE[seg_addr];
   
endmodule
