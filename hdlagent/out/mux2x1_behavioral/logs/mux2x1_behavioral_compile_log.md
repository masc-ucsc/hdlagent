# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Design and Implement a 2:1 Multiplexer using Behavioral Modeling the inputs are `a` and `b` and `select`, and the output is `y`.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The module declaration is: module mux2x1_behavioral(input  [0:0] a,input  [0:0] b,input  [0:0] select,output  [0:0] reg y);


**Assistant:**
```verilog
module mux2x1_behavioral(
    input [0:0] a,
    input [0:0] b,
    input [0:0] select,
    output reg [0:0] y
);

always @(*) begin
    if (select == 1'b0)
        y = a;
    else
        y = b;
end

endmodule
```

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : mux2x1_behavioral : 1 : 0 : 1 : 0 : 138 : 84 : 1.6113159656524658 : 1.5070562362670898