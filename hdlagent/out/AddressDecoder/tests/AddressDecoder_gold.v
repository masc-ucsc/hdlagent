module AddressDecoder (
    input [31:0] addr,
    output reg synap_matrix,
    output reg [4:0] param_num,
    output reg neuron_spike_out,
    output reg param
);

    always @(addr) begin
    synap_matrix = 0;
        param = 0;
        param_num = 5'b0;
        neuron_spike_out = 0;

       case(addr[14:13])
            2'b00: synap_matrix = 1;
            2'b01: begin
                param = 1;
                param_num = addr[8:4];
            end
            2'b10: neuron_spike_out = 1;
            default: ;
        endcase
    end

endmodule


