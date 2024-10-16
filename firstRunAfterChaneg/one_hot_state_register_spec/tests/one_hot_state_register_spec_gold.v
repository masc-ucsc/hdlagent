module ScalarRegisterFile #(
    parameter NUM_PORTS = 1,
    parameter ADDR_WIDTH = 5,
    parameter DATA_WIDTH = 32,
    parameter NUM_REGISTERS = 32
) (
    input logic clk,
    input logic [DATA_WIDTH-1:0] recv_msg,
    input logic [ADDR_WIDTH-1:0] recv_idx,
    input logic recv_val,
    output logic recv_rdy,
    input logic [ADDR_WIDTH*NUM_PORTS-1:0] send_idx_flat,
    output logic [DATA_WIDTH*NUM_PORTS-1:0] send_msg_flat,
    output logic [NUM_PORTS-1:0] send_val,
    input logic [NUM_PORTS-1:0] send_rdy
);

    logic [DATA_WIDTH-1:0] reg_file[NUM_REGISTERS-1:0];

    assign recv_rdy = 1'b1;

    always_ff @(posedge clk) begin
        if (recv_val) begin
            reg_file[recv_idx] <= recv_msg;
        end
    end

    genvar i;
    generate
        for (i = 0; i < NUM_PORTS; i = i + 1) begin : read_ports
            wire [ADDR_WIDTH-1:0] send_idx = send_idx_flat[ADDR_WIDTH*i +: ADDR_WIDTH];
            always_ff @(posedge clk) begin
                if (send_rdy[i]) begin
                    send_msg_flat[DATA_WIDTH*i +: DATA_WIDTH] <= reg_file[send_idx];
                    send_val[i] <= 1'b1;
                end else begin
                    send_val[i] <= 1'b0;
                end
            end
        end
    endgenerate
endmodule

