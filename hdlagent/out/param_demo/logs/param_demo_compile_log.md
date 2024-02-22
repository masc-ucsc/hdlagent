# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Design a module that utilizes both a parameter and a localparam to set a 4-bit output 'o' to a specific value. The parameter should be the value 9, and the localparam should be value of the parameter plus one. 'o' will take the value of the localparam.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be param_demo


**Assistant:**
module param_demo (
    output reg [3:0] o
);
  
  parameter VALUE = 9;
  localparam NEXT_VALUE = VALUE + 1;
  
  always @* begin
    o = NEXT_VALUE;
  end
  
endmodule

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : param_demo : 1 : 0 : 1 : 0 : 129 : 52 : 1.3706765174865723 : 1.3170716762542725