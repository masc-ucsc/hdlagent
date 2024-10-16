module universal_shift_register_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] shift_dir,
    input [0:0] shift_mode,
    input [3:0] data_in,
    input [0:0] data_in_serial,
    output reg [3:0] q
);
    
    always @(posedge clock) begin
        if (reset) begin
            q <= 4'b0000;  // Reset the output to 0
        end else begin
            if (shift_mode) begin
                q <= data_in; // Parallel load
            end else begin
                if (shift_dir) begin
                    q <= {data_in_serial, q[3:1]}; // Right shift
                end else begin
                    q <= {q[2:0], data_in_serial}; // Left shift
                end
            end
        end
    end

endmodule
