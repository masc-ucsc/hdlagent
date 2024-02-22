# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Create a module that showcases a wire 'w' being driven by two continuous assignments. The inputs: [0:0]a, [0:0]b, [0:0]sel and the outputs: [0:0]w, [0:0]w1, [0:0]w2. 'w1' is the bitwise AND of 'a' and 'b', while 'w2' is the bitwise OR of 'a' and 'b'. 'w' will be set to the value of 'w1' when 'sel' is high, and the value of 'w2' when 'sel' is low.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be wire_drive_demo


**Assistant:**
```verilog
module wire_drive_demo(input [0:0] a, input [0:0] b, input [0:0] sel, output reg [0:0] w, output reg [0:0] w1, output reg [0:0] w2);

always @(*)
begin
    w1 = a & b;
    w2 = a | b;
    if(sel)
        w = w1;
    else
        w = w2;
end

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : wire_drive_demo : 1 : 0 : 1 : 0 : 205 : 108 : 5.972370624542236 : 5.904142141342163