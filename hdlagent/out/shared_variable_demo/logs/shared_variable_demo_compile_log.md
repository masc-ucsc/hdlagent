# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Implement a module with two always blocks that share a common variable 'shared_var'. The input: [7:0]a and the outputs: [7:0]o, [7:0]shared_var. The fireset block should update 'shared_var' with input 'a', and the second block should set output 'o' to 'shared_var'.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be shared_variable_demo


**Assistant:**
```verilog
module shared_variable_demo (
    input [7:0] a,
    output [7:0] o,
    output [7:0] shared_var
);

reg [7:0] shared_var;

always @* begin
    shared_var = a;
end

always @* begin
    o = shared_var;
end

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : shared_variable_demo : 1 : 0 : 1 : 0 : 143 : 77 : 1.8599202632904053 : 1.7867677211761475