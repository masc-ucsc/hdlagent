# Spec Conversation

**User:**

Rewrite the following RTL program description into a formal specification document, focusing on clarity and maintaining specific details. The format should be a bullet point list written in natural english, and should be as long as the description is complex. Do not response with ANYTHING BESIDES the bullet point list. Maintain the module and IO names exactly as they were stated in my original description:
Design a module that takes 8 bit signed inputs 'a' and 'b' and has outputs 'div' and 'mod' which are the 6 bit truncated signed results of 'a' by 'b' division and modulus operations, respectively.


**Assistant:**
- Design a module with the following specifications:
  - The module accepts two inputs:
    - Input 'a': an 8-bit signed integer.
    - Input 'b': an 8-bit signed integer.
  - The module provides two outputs:
    - Output 'div': a 6-bit truncated signed integer representing the result of division of 'a' by 'b'.
    - Output 'mod': a 6-bit truncated signed integer representing the result of the modulus operation of 'a' by 'b'.
  - The output 'div' should be calculated by performing an integer division of 'a' by 'b' and then truncating the result to fit 6 bits.
  - The output 'mod' should be calculated by performing a modulus operation on 'a' with respect to 'b' and then truncating the result to fit 6 bits.
  - All arithmetic operations are based on signed integers.
  - Truncation for fitting into 6 bits should preserve the sign of the result.

**User:**

Write a Verilog module interface for the previous program description. Respond with nothing else but a SINGLE LINE code block that is the module interface declaration, without any comments or additional english explanation. Maintain the module and IO names exactly as they were stated in my original description and declare the port directions as input or output, do NOT put 'endmodule'.


**Assistant:**
```verilog
module calculate_div_mod (input signed [7:0] a, input signed [7:0] b, output signed [5:0] div, output signed [5:0] mod);
```

