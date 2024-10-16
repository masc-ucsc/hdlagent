module PredicateRegisterFile #(parameter WIDTH=32, DEPTH=32)
(
    input logic clk,
    input logic [WIDTH-1:0] recv_msg,
    input logic [4:0] recv_idx,
    input logic recv_val,
    output logic recv_rdy,

    output logic [WIDTH-1:0] send_msg,
    output logic [4:0] send_idx,
    output logic send_val,
    input logic send_rdy
);

       logic [WIDTH-1:0] reg_file [0:DEPTH-1];

      logic [4:0] write_ptr;

        logic [4:0] read_ptr;

     logic write_en;

       logic read_en;

       always_ff @(posedge clk) begin
        if (recv_val && recv_rdy) begin
            reg_file[recv_idx] <= recv_msg;
            write_ptr <= recv_idx;
        end
    end

       always_ff @(posedge clk) begin
        if (send_val && send_rdy) begin
            send_msg <= reg_file[read_ptr];
            send_idx <= read_ptr;
        end
    end

       assign recv_rdy = 1'b1; assign send_val = 1'b1;
endmodule

