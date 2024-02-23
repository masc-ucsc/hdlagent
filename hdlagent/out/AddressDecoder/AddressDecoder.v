module AddressDecoder(
    input  [31:0] addr,
    output reg synap_matrix,
    output reg [4:0] param_num,
    output reg neuron_spike_out,
    output reg param
);

    // Bit 14:13 used for Block Decoding
    always @* begin
        synap_matrix = (addr[14:13] == 2'b00);       // synap_matrix block
        param = (addr[14:13] == 2'b01);              // param block
        neuron_spike_out = (addr[14:13] == 2'b10);   // neuron_spike_out block 
    end

    always @* begin
        if(param)                             // If Block is param
            param_num = addr[8:4];          // Take Bit 8:4 for param module number
        else
            param_num = 0;                  // Else output 0
    end
endmodule