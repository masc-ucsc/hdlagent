# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Design a 4:1 Multiplexer(Mux). The inputs are in0, in1, in2, in3 and 2-bit `sel` one-bit output `out_o`.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The module declaration is: module mux4to1(output  [0:0] out_o,input  [0:0] in0,input  [0:0] in1,input  [0:0] in2,input  [0:0] in3,input  [1:0] sel);


**Assistant:**
module mux4to1(
    output [0:0] out_o,
    input [0:0] in0,
    input [0:0] in1,
    input [0:0] in2,
    input [0:0] in3,
    input [1:0] sel
);

assign out_o = (sel[1]) ? (sel[0] ? in3 : in2) : (sel[0] ? in1 : in0);

endmodule


**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : mux4to1 : 1 : 0 : 1 : 0 : 161 : 104 : 1.4870326519012451 : 1.379150390625