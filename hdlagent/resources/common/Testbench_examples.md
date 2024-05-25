**System:** You are an code generation agent expert in Verilog design verification that writes only testbenches for the Icarus Verilog simulator, which only supports Verilog 1995, 2001, and 2005. Do not write explanations, just code.

**User:** I have a Verilog module named 'nor_reduction' that takes a 8-bit input 'bus_i' and has a 1-bit output 'reduce_o' which is the NOR reduction of 'bus_i'. Write an assertion based Verilog testbench for this module. Assert statements should test both simple and corner cases of the implementation for functional correctness.

**Assistant:** ```
module nor_reduction_tb;

  // Test Inputs
  reg [7:0] bus_i;

  // Test Outputs
  wire out;

  // Instantiate the Unit Under Test (UUT)
  nor_reduction uut (
    .bus_i(bus_i),
    .out(out)
  );

  // Test sequence
  initial begin

    // Simple case for any 1's in the input, for loop will wrap around to 0, ending it
    for (bus_i = 1; bus_i > 0; bus_i = bus_i + 1) begin
      #10;
      assert(out === 0) else $error("Test failed for input: %d, expected output: 0, got: %b", bus_i, out);
    end

    // Test for input value 0
    bus_i = 0;
    #10;
    assert(out === 1) else $error("Test failed for input: 0, expected output: 1, got: %b", out);

    // Finish test
    $finish;
  end

endmodule
```

**User:** I have a Verilog module named 'odds_evens_sum' that takes a 7-bit input 'in_i' and has three outputs. 'odds_o' is 3-bits wide and is the odd-numbered bits from the input, concatenated in order. Conversely, 'evens_o' is 4-bits wide and is the even-numbered bits. The last output 'sum_o' is the 5-bit wide sum of 'odds_o' and 'evens_o'. Write an assertion based Verilog testbench for this module. Assert statements should test both simple and corner cases of the implementation for functional correctness.

**Assistant:** ```
module odds_evens_sum_tb;

  // Test Inputs
  reg [6:0] in_i;

  // Test Outputs
  wire [2:0] odds_o;
  wire [3:0] evens_o;
  wire [4:0] sum_o;

  // Instantiate the Unit Under Test (UUT)
  odds_evens_sum uut (
    .in_i(in_i),
    .odds_o(odds_o),
    .evens_o(evens_o),
    .sum_o(sum_o)
  );

  // Set continuous property checks, end simulation on first failure
  always@(*) begin
    assert (sum_o === odds_o + evens_o) else begin $error("Property check failed for input: %d, odds_o + evens_o != sum_o", in_i); $finish; end
  end

  // Test sequence
  initial begin

    // Simple case for all 1's
    in_i = 127;
    #10;
    assert(odds_o === 7) else $error("Test failed for input: 127, expected odds_o: 111, got: %b", odds_o);
    assert(evens_o === 15) else $error("Test failed for input: 127, expected evens_o: 1111, got: %b", evens_o);

    // Simple case for all 0's
    in_i = 0;
    #10;
    assert(odds_o === 0) else $error("Test failed for input: 0, expected odds_o: 000, got: %b", odds_o);
    assert(evens_o === 0) else $error("Test failed for input: 0, expected evens_o: 0000, got: %b", evens_o);

    // Simple case of half 1's and half 0's
    in_i = 7'b000_1111;
    #10;
    assert(odds_o === 3) else $error("Test failed for input: 7'b000_1111, expected odds_o: 011, got: %b", odds_o);
    assert(evens_o === 3) else $error("Test failed for input: 7'b000_1111, expected evens_o: 0011, got: %b", evens_o);

    // Complex cases for interleaved 1's and 0's
    in_i = 7'b101_0101;
    #10;
    assert(odds_o === 0) else $error("Test failed for input: 7'b101_0101, expected odds_o: 0000, got: %b", odds_o);
    assert(evens_o === 15) else $error("Test failed for input: 7'b101_0101, expected evens_o: 1111, got: %b", evens_o);

    in_i = 7'b010_1010;
    #10;
    assert(odds_o === 7) else $error("Test failed for input: 7'b010_1010, expected odds_o: 111, got: %b", odds_o);
    assert(evens_o === 0) else $error("Test failed for input: 7'b010_1010, expected evens_o: 0000, got: %b", evens_o);

    // Finish test
    $finish;
  end

endmodule
```

**User:** I have a Verilog module named 'simple_alu' that implements an Arithmetic Logic Unit which has three inputs: 'rs1_i' and 'rs2_i' are both 8-bit wide value inputs, and 'op_i' is a 2-bit wide opcode input, which determines the operation performed on 'rs1_i' and 'rs2_i'. The function has a single 8-bit output 'result_o', which is set to the sum of the inputs when the opcode is 0, the difference of the inputs when the opcode is 1, and the product of the inputs when the opcode is 2. No other operations are supported, so if an unknown opcode is detected, the output is set to zero. Write an assertion based Verilog testbench for this module. Assert statements should test both simple and corner cases of the implementation for functional correctness.

**Assistant:** ```
module simple_alu_tb;

  // Test Inputs
  reg [7:0] rs1_i;
  reg [7:0] rs2_i;
  reg [1:0] op_i;

  // Test values, add an extra bit to end the for loop
  reg [8:0] rs1_val;
  reg [8:0] rs2_val;
  reg [2:0] op_val;

  assign rs1_i = rs1_val[7:0];
  assign rs2_i = rs2_val[7:0];
  assign op_i  = op_val[1:0];

  // Test Outputs
  wire [7:0] result_o;

  // Instantiate the Unit Under Test (UUT)
  simple_alu uut (
    .rs1_i(rs1_i),
    .rs2_i(rs2_i),
    .op_i(op_i),
    .result_o(result_o)
  );

  // Define operation codes
  localparam ADD = 2'b00;
  localparam SUB = 2'b01;
  localparam MUL = 2'b10;

  // Continuous property checks, end simulation on first failure
  always @(*) begin
    #10; // same delay as for loop(s)
    case (op_i)
      ADD: assert (result_o === rs1_i + rs2_i) else begin $error("Test failed for ADD, rs1_i: %b, rs2_i: %b, expected result_o: %b, got: %b", rs1_i, rs2_i, rs1_i + rs2_i, result_o); $finish; end
      SUB: assert (result_o === rs1_i - rs2_i) else begin $error("Test failed for SUB, rs1_i: %b, rs2_i: %b, expected result_o: %b, got: %b", rs1_i, rs2_i, rs1_i - rs2_i, result_o); $finish; end
      MUL: assert (result_o === rs1_i * rs2_i) else begin $error("Test failed for MUL, rs1_i: %b, rs2_i: %b, expected result_o: %b, got: %b", rs1_i, rs2_i, rs1_i * rs2_i, result_o); $finish; end
      default: assert (result_o === 0) else begin $error("Test failed for unknown op_i, expected result_o: 0, got: %b", result_o); $finish; end
    endcase
  end

  // Test sequence
  initial begin

    // Simple case for testing add, sub, and mult functionally
    for (rs1_val = 0; rs1_val[8] != 1; rs1_val = rs1_val + 1) begin     // check MSB to end for loop
      for (rs2_val = 0; rs2_val[8] != 1; rs2_val = rs2_val + 1) begin
        for (op_val = 0; op_val[2] != 1; op_val = op_val + 1) begin
          #10;  // property checks happen
        end
      end
    end

    // Finish test
    $finish;
  end

endmodule
```

**User:** I have a Verilog module that uses a compile loop to add up the values from 7 to 11. The name should be 'add_7_to_11' and has 16-bit output 'res_o'. Write an assertion based Verilog testbench for this module. Assert statements should test both simple and corner cases of the implementation for functional correctness.

**Assistant:** ```
module add_7_to_11_tb;

  // Test Outputs
  wire [15:0] res_o;

  // Instatitate the Unit Under Test (UUT)
  add_7_to_11 uut (
    .res_o(res_o)
  );

  // Test sequence
  initial begin

    // Basic test for checking const value
    #10;
    assert (res_o === 7 + 8 + 9 + 10 + 11) else $error("Test failed, value mismatch, expected: %b, got: %b", 7 + 8 + 9 + 10 + 11, res_o);  // unroll the accumulative loop

    // Finish test
    $finish;
  end

endmodule
```

**User:** I have a Verilog module that is a naive implementation of the RISC-V FMAdd instruction, where the opcode is as listed in the official spec, but any FP rules are ignored as well as the RM and FMT fields. The source operands will take on the values of their register numbers. The 'result' output will be the multiply-add operation, and the 'rd' output will be the decoded destination register. If the opcode is incorrect, then the 'err' output must be set and the other outputs must be cleared. The module declaration is 'module fmadd(input [31:0] instruction, output [4:0] rd, output [31:0] result, output err);' Write an assertion based Verilog testbench for this module. Assert statements should test both simple and corner cases of the implementation for functional correctness.

**Assistant:** ```
module fmadd_tb;

  // Test inputs
  reg [31:0] instruction;

  // Test values, add an extra bit to end the for loop
  reg [32:0] instruction_val;

  assign instruction = instruction_val[31:0];

  // Test outputs
  wire [4:0] rd;
  wire [31:0] result;
  wire err;

  // Instantiate the Unit Under Test (UUT)
  fmadd uut (
    .instruction(instruction),
    .rd(rd),
    .result(result),
    .err(err)
  );

  // Intermediate signals
  wire [6:0] opcode = instruction[6:0];
  wire [4:0] rs1 = instruction[19:15];
  wire [4:0] rs2 = instruction[24:20];
  wire [4:0] rs3 = instruction[31:27];

  // Expected, correct, opcode for FMADD operation
  localparam FMADD_OPCODE = 7'b1000011;

  // Continuous property checks, end simulation on first failure
  always @(*) begin
    #10; // same delat as for loop
    if (opcode == FMADD_OPCODE) begin
      assert (rd === instruction[11:7]) else begin $error("Test failed, instruction: %b, expected rd: %b, got: %b", instruction, instruction[11:7], rd); $finish; end
      assert (result === rs1 * rs2 + rs3) else begin $error("Test failed, instruction: %b, expected result: %b, got: %b", instruction, rs1 * rs2 + rs3, result); $finish; end
      assert (err === 1'b0) else begin $error("Test failed, instruction: %b, expected err: 0, got: 1"); $finish; end
    end else begin
      assert (rd === 0) else begin $error("Test failed, instruction: %b, expected rd: 0, got: %b", instruction, rd); $finish; end
      assert (result === 0) else begin $error("Test failed, instruction: %b, expected result: 0, got: %b", instruction, result); $finish; end
      assert (err === 1'b1) else begin $error("Test failed, instruction: %b, expected err: 1, got: 0"); $finish; end
    end
  end

  // Test sequence
  initial begin

    // Increment by 2345, since increment by 1 will result in a very long simulation for a 2^32 validation
    for (instruction_val = 0; instruction_val[32] != 1; instruction_val = instruction_val + 2345) begin
      #10;  // property checks happen
    end
    //Finish test
    $finish;
  end

endmodule
```
