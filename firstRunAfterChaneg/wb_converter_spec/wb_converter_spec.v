module wb_converter_spec(
    input [0:0] wb_clk_i,
    input [0:0] wb_rst_i,
    input [0:0] wbs_stb_i,
    input [0:0] wbs_cyc_i,
    input [0:0] wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output logic [0:0] wbs_ack_o,
    output logic [31:0] wbs_dat_o,
    output logic [63:0] load_recv_msg,
    output logic [0:0] load_recv_val,
    input [0:0] load_recv_rdy,
    output logic [31:0] instruction_recv_msg,
    output logic [0:0] instruction_recv_val,
    input [0:0] instruction_recv_rdy,
    input [31:0] store_send_msg,
    input [0:0] store_send_val,
    output logic [0:0] store_send_rdy
);

// Acknowledge logic
assign wbs_ack_o = wbs_stb_i & wbs_cyc_i & (instruction_recv_rdy | load_recv_rdy);

// Instruction transaction
assign instruction_recv_val = (wbs_adr_i == 32'h30000000) & wbs_stb_i & wbs_cyc_i;
assign instruction_recv_msg = (wbs_adr_i == 32'h30000000) ? wbs_dat_i : 32'b0;

// Load transaction
assign load_recv_val = (wbs_adr_i >= 32'h30000004) & wbs_stb_i & wbs_cyc_i & ~wbs_we_i;
assign load_recv_msg = {32'b0, wbs_dat_i} - 64'h30000004;

// Store transaction readiness
assign store_send_rdy = wbs_stb_i & wbs_cyc_i & wbs_we_i & load_recv_rdy;

// Data output
assign wbs_dat_o = (wbs_adr_i >= 32'h30000004 & wbs_we_i) ? store_send_msg : 32'b0;

endmodule
