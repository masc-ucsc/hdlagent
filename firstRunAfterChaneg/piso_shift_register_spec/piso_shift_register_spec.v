module piso_shift_register_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] load,
    input [3:0] data_in_parallel,
    output [0:0] data_out_serial
);
    reg [3:0] shift_register;

    assign data_out_serial = shift_register[3];
    
    always @ (posedge clock or posedge reset) begin
        if (reset) begin
            shift_register <= 4'b0000;
        end else if (load) begin
            shift_register <= data_in_parallel;
        end else begin
            shift_register <= {shift_register[2:0], 1'b0};
        end
    end
endmodule
