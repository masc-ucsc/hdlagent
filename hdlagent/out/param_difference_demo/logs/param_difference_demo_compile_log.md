# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Create a module that demonstrates the difference between a `parameter` and a `localparam`. The parameters value should be 10 and the local parameters value should be one greater than that. Set 'o' to the value of the local parameter. The module has one output 4-bit `o`
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be param_difference_demo


**Assistant:**
```verilog
module param_difference_demo (
    output reg [3:0] o
);

parameter value = 10;
localparam local_value = value + 1;

assign o = local_value;

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : param_difference_demo : 1 : 0 : 1 : 0 : 129 : 46 : 1.1759560108184814 : 1.1145873069763184