# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Implement a module which takes a 4-bit input 'a' and outputs 'o' as 1 if 'a' is equal to a binary literal of value 11.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be binary_literal_demo


**Assistant:**
```verilog
module binary_literal_demo (
    input [3:0] a,
    output o
);
assign o = (a == 4'b1011) ? 1'b1 : 1'b0;
endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : binary_literal_demo : 1 : 0 : 1 : 0 : 105 : 50 : 1.1962015628814697 : 1.126368522644043