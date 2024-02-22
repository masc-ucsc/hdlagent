module fmultiplier_comb(
    input  [31:0] a,
    input  [31:0] b,
    output reg [31:0] z
);

// Extract fields from inputs
wire [31:0] a1 = a[30:23] == 8'd255 ? a[22:0] != 0 ? 32'hffc00000 : a : a[30] << 31 | (a[30:23] + 8'd127) << 23 | a[22:0];   
wire [31:0] b1 = b[30:23] == 8'd255 ? b[22:0] != 0 ? 32'hffc00000 : b : b[30] << 31 | (b[30:23] + 8'd127) << 23 | b[22:0];

// Handle multiplication logic
wire [62:0] m_pro = (a1[30:0] * b1[30:0]) << 1;   
wire [47:0] m_norm = m_pro[62] || m_pro[61] ? m_pro[61:10] + {1'b0, m_pro[9], m_pro[8:0] != 10'h200 && m_pro[8:0] != 10'h000} : m_pro[60:9] + {1'b0, m_pro[8], m_pro[7:0] != 9'h100 && m_pro[7:0] != 9'h000};
wire [ 8:0] e_norm = m_pro[62] || m_pro[61] ? a1[30:23] + b1[30:23] : a1[30:23] + b1[30:23] - 1'd1;

// Handle rounding
wire [32:0] f_norm = e_norm[8] ? 32'h7F800000 : e_norm[7] ? 32'hFF800000 : m_norm[46] ? {1'b0, 47'h00001}+ { 1'b0, e_norm, m_norm[45:23], m_norm[22] } : {1'b0, 47'h00001} + { 1'b0, e_norm, m_norm[45:23] };
assign z = a1[31] ^ b1[31] ? f_norm + 32'h80000000 : f_norm;

endmodule