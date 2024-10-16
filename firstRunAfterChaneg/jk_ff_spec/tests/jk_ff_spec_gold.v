module VectorRegisterFile #(
    parameter NUM_READ_PORTS = 2,
    parameter NUM_WRITE_PORTS = 2
) (
    input wire clk,
    input wire reset,
    input wire [31:0] recv_msg_0,
    input wire [31:0] recv_msg_1,
    input wire [9:0] recv_index_0,
    input wire [9:0] recv_index_1,
    input wire recv_val_0,
    input wire recv_val_1,
    output wire recv_rdy_0,
    output wire recv_rdy_1,
    output wire [31:0] send_msg_0,
    output wire [31:0] send_msg_1,
    output wire [9:0] send_index_0,
    output wire [9:0] send_index_1,
    output wire send_val_0,
    output wire send_val_1,
    output wire send_rdy_0,
    output wire send_rdy_1
);

    reg [31:0] register_file [31:0][31:0];

    always @(posedge clk) begin
        if (reset) begin
            integer i, j;
            for (i = 0; i < 32; i = i + 1) begin
                for (j = 0; j < 32; j = j + 1) begin
                    register_file[i][j] <= 32'b0;
                end
            end
        end
        else begin
            if (recv_val_0 && recv_rdy_0) begin
                register_file[recv_index_0[4:0]][recv_index_0[9:5]] <= recv_msg_0;
            end
            if (recv_val_1 && recv_rdy_1) begin
                register_file[recv_index_1[4:0]][recv_index_1[9:5]] <= recv_msg_1;
            end
        end
    end

    assign send_msg_0 = register_file[send_index_0[4:0]][send_index_0[9:5]];
    assign send_val_0 = (send_index_0 < 1024);
    assign send_rdy_0 = 1'b1;

    assign send_msg_1 = register_file[send_index_1[4:0]][send_index_1[9:5]];
    assign send_val_1 = (send_index_1 < 1024);
    assign send_rdy_1 = 1'b1;

    assign recv_rdy_0 = 1'b1;
    assign recv_rdy_1 = 1'b1;

endmodule

