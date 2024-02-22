module AddressDecoder(
    input  [31:0] addr,
    output reg synap_matrix,
    output reg [4:0] param_num,
    output reg neuron_spike_out,
    output reg param
);
  
  //  Define position of the address bits used for decoding
  localparam phase_decoder = 2'b00, 
             param_decoder = 2'b01, 
             neuron_decoder = 2'b10;

  //  Use segments of the address bits to determine major blocks
  assign synap_matrix = (addr[14:13] == phase_decoder) ? 1 : 0;          //  Synap Matrix
  assign param = (addr[14:13] == param_decoder) ? 1 : 0;                 //  Param Modules
  assign neuron_spike_out = (addr[14:13] == neuron_decoder) ? 1 : 0;    //  Neuron Spike Out

  //  Use segments of the address bits to determine specific param
  always@*
  begin
    if (param) // If param block
    begin
      param_num = addr[8:4]; // Get specific param index
    end
    else
    begin
      param_num = 5'b0; //  Set to 0 as default
    end
  end

endmodule