# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Implement a module that encodes a 2-bit input '[1:0]a' into a 4-bit one-hot encoded output '[3:0]one_hot'.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be one_hot_encoder


**Assistant:**
```verilog
module one_hot_encoder(
    input [1:0] a,
    output reg [3:0] one_hot
);
always @(*)
    case(a)
        2'b00: one_hot = 4'b0001;
        2'b01: one_hot = 4'b0010;
        2'b10: one_hot = 4'b0100;
        2'b11: one_hot = 4'b1000;
        default: one_hot = 4'b0000;
    endcase
endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : one_hot_encoder : 1 : 0 : 1 : 0 : 104 : 118 : 5.41897177696228 : 5.358955383300781