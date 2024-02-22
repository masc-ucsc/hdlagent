# Compile Conversation

**User:**
Can you implement the described Module in Verilog using purely combinational logic:
Create a module which computes the bitwise XOR operation. Inputs: [7:0]a, [7:0]b. Outputs: [7:0]o.
Please respond with only valid program syntax. Set input/output names exactly as stated, avoid abbreviation. Please do not provide any additional English explanation, short comments in the code are allowed.
The name of the module should be bitwise_xor


**Assistant:**
module bitwise_xor(
  input [7:0] a,
  input [7:0] b,
  output reg [7:0] o
);

always @ (*) begin
  o = a ^ b;
end

endmodule

**System:**
Success!
After 0 compilation failures and 0 testing failures, your desired circuit was generated!


RESULTS : bitwise_xor : 1 : 0 : 1 : 0 : 103 : 49 : 1.6328134536743164 : 1.5671563148498535