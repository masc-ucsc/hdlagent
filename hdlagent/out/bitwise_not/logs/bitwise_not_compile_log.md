# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Develop a module that inverts the bits. Inputs: [7:0]a. Outputs: [7:0]o.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be bitwise_not


**Assistant:**
```verilog
module bitwise_not(
    input [7:0] a,
    output [7:0] o
);

assign o = ~a;

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : bitwise_not : 1 : 0 : 1 : 0 : 95 : 37 : 2.243321657180786 : 2.1924052238464355