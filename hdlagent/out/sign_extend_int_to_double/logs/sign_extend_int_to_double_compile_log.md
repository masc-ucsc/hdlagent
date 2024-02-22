# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Implement a module that sign extends an input int sized wire 'int_i[31:0]' to an output double sized wire 'double_o[63:0]'. Input(s): int_i[31:0]. Output(s): double_o[63:0].
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The module declaration is: module sign_extend_int_to_double(input  [31:0] int_i,output  [63:0] double_o);


**Assistant:**
```verilog
module sign_extend_int_to_double(
  input [31:0] int_i,
  output [63:0] double_o
);
  
  assign double_o = {{32{int_i[31]}}, int_i};

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : sign_extend_int_to_double : 1 : 0 : 1 : 0 : 142 : 54 : 1.2787165641784668 : 1.2561678886413574