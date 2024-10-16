module ScalarRegisterFile_spec
#(
  parameter NUM_PORTS = 1
)
(
  input logic clk,
  input logic [31:0] recv_msg,
  input logic [4:0] recv_idx,
  input logic recv_val,
  output logic recv_rdy,
  input logic [4:0] send_idx [NUM_PORTS-1:0],
  output logic [31:0] send_msg [NUM_PORTS-1:0],
  output logic send_val [NUM_PORTS-1:0],
  input logic send_rdy [NUM_PORTS-1:0]
);

  // Register file storage
  logic [31:0] reg_file [31:0];

  // Write logic
  always_comb begin
    if (recv_val) begin
      reg_file[recv_idx] = recv_msg;
    end
  end

  // Calculate recv_rdy
  assign recv_rdy = ~recv_val;

  // Read logic
  genvar i;
  generate
    for (i = 0; i < NUM_PORTS; i = i + 1) begin
      always_comb begin
        if (send_rdy[i]) begin
          send_msg[i] = reg_file[send_idx[i]];
          send_val[i] = 1'b1;
        end else begin
          send_msg[i] = 32'b0;
          send_val[i] = 1'b0;
        end
      end
    end
  endgenerate

endmodule
