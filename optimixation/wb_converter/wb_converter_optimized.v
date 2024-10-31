module wb_converter (
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output logic wbs_ack_o,
    output [31:0] wbs_dat_o,

    output logic [63:0] load_recv_msg,
    output logic load_recv_val,
    input load_recv_rdy,

    output logic [31:0] instruction_recv_msg,
    output logic instruction_recv_val,
    input instruction_recv_rdy,

    input [31:0] store_send_msg,
    input store_send_val,
    output logic store_send_rdy
);

    logic ack_condition;
    logic instruction_condition;
    logic load_store_address;

    assign ack_condition = wbs_cyc_i && wbs_stb_i;
    assign instruction_condition = wbs_adr_i == 32'h30000000;
    assign load_store_address = wbs_adr_i > 32'h30000000;

    assign wbs_ack_o = ack_condition && (
                         (instruction_condition && instruction_recv_rdy) || 
                         (load_store_address && wbs_we_i && load_recv_rdy && instruction_recv_rdy) || 
                         (load_store_address && !wbs_we_i && store_send_val && store_send_rdy)
                       );

    assign store_send_rdy = ack_condition && !wbs_we_i && load_store_address;
    assign wbs_dat_o = store_send_msg;

    always_comb begin
        load_recv_msg = 64'b0;
        load_recv_val = 0;
        instruction_recv_msg = 32'b0;
        instruction_recv_val = 0;

        if (instruction_condition) begin
            instruction_recv_msg = wbs_dat_i;
            instruction_recv_val = ack_condition;
        end else if (load_store_address) begin
            load_recv_msg = {(wbs_adr_i - 32'h30000004) >> 2, wbs_dat_i};           
            load_recv_val = ack_condition;
            if (wbs_we_i) begin
                instruction_recv_msg = 32'd0;
            end else begin
                instruction_recv_msg = {5'b00001, 27'b0};
            end
            instruction_recv_val = ack_condition;
        end
    end

endmodule
