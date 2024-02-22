# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Implement a module that computes both the sum and difference of two 4-bit inputs 'a' and 'b' concurrently, producing two 4-bit outputs 'sum' and 'diff'. The inputs: [3:0]a, [3:0]b and the outputs: [3:0]sum, [3:0]diff.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be concurrent_arithmetic


**Assistant:**
```verilog
module concurrent_arithmetic(
    input [3:0] a,
    input [3:0] b,
    output reg [3:0] sum,
    output reg [3:0] diff
);

always @(*) begin
    sum = a + b;
    diff = a - b;
end

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : concurrent_arithmetic : 1 : 0 : 1 : 0 : 141 : 73 : 1.6195392608642578 : 1.5767297744750977