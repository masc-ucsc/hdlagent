module VectorRegisterFile_spec(
    input [0:0] clk,
    input [0:0] reset,
    input [31:0] recv_msg_0,
    input [31:0] recv_msg_1,
    input [9:0] recv_index_0,
    input [9:0] recv_index_1,
    input [0:0] recv_val_0,
    input [0:0] recv_val_1,
    output [0:0] recv_rdy_0,
    output [0:0] recv_rdy_1,
    output [31:0] send_msg_0,
    output [31:0] send_msg_1,
    input [9:0] send_index_0,
    input [9:0] send_index_1,
    output [0:0] send_val_0,
    output [0:0] send_val_1,
    output [0:0] send_rdy_0,
    output [0:0] send_rdy_1
);

    // 32x32 register file, each of 32-bit width
    reg [31:0] regfile [31:0][31:0]; // Declare as [31:0] for both dimensions for correct indexing
    integer i, j;

    // Always ready to receive
    assign recv_rdy_0 = 1'b1;
    assign recv_rdy_1 = 1'b1;

    // Always ready to send
    assign send_rdy_0 = 1'b1;
    assign send_rdy_1 = 1'b1;

    // Write logic
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            for (i = 0; i < 32; i = i + 1) begin
                for (j = 0; j < 32; j = j + 1) begin
                    regfile[i][j] <= 32'b0;
                end
            end
        end else begin
            if (recv_val_0) begin
                regfile[recv_index_0[9:5]][recv_index_0[4:0]] <= recv_msg_0;
            end
            if (recv_val_1) begin
                regfile[recv_index_1[9:5]][recv_index_1[4:0]] <= recv_msg_1;
            end
        end
    end

    // Read logic
    assign send_msg_0 = regfile[send_index_0[9:5]][send_index_0[4:0]];
    assign send_msg_1 = regfile[send_index_1[9:5]][send_index_1[4:0]];

    // Valid signals for reading
    assign send_val_0 = (send_index_0 < 1024) ? 1'b1 : 1'b0;
    assign send_val_1 = (send_index_1 < 1024) ? 1'b1 : 1'b0;

endmodule
