# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Design a module that uses a localparam to set an 8-bit output 'o' to a constant value of 8'b10101010..
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be constant_demo


**Assistant:**
```verilog
module constant_demo (
    output reg [7:0] o
);

localparam constant_value = 8'b10101010;

always @* begin
    o = constant_value;
end

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : constant_demo : 1 : 0 : 1 : 0 : 98 : 48 : 3.6157658100128174 : 3.5279457569122314