# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
The module, named `AddressDecoder` for address decoding will have: 1-A 32-bit input for the address. 2-Outputs to indicate which module the address corresponds to. 3-An output to represent the index in case of a param module. Memory Map: 1: Address Range: `0x30000000 - 0x30003FFF`. Address Identification: Bits `[14:13] = 2'b00`. 2: ** modules (32 modules, each of 12 bytes, but aligned to 16 bytes):** Total Address Range for all `param` modules: `0x30004000 - 0x300040FF` Address Identification for the param range: Bits `[14:13]` = `2'b01`. param0 : `0x30004000 - 0x3000400B`. param1 : `0x30004010 - 0x3000401B` ... param31 : `0x3000401E0 - 0x3000401EB`. Specific `param` Identification: Bits `[8:4]`. This will yield values ranging from `5'b00000` (0 in decimal) for `param0` to `5'b11111` (31 in decimal) for `param31`. 3: Address Range: `0x30008000 - 0x30008003` Address Identification: Bits `[14:13]` = `2'b10`. Decoder Identification Bits: To determine the major block: Check bits `[14:13]`:/n `2'b00`: `synap_matrix` /n `2'b01`: `param` modules/n `2'b10`: `neuron_spike_out`/n To determine the specific param:/n If `[14:13]` indicates a `param` block, then bits `[8:4]` will give the specific `param` index (from `param0` to `param31`)./n With this setup, the memory map provides an efficient way to decode addresses for each block using bitwise operations. 
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The module declaration is: module AddressDecoder(input  [31:0] addr,output  [0:0] reg synap_matrix,output  [0:0] reg [4:0] param_num,output  [0:0] reg neuron_spike_out,output  [0:0] reg param);


**Assistant:**
```verilog
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
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : AddressDecoder : 1 : 0 : 1 : 0 : 1 : 553 : 288 : 7.624261140823364 : 7.581974744796753