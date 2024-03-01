**User:** - Modules:
  - Example 1: Simple Adder Module
    ```
    module adder(input a, input b, output sum);
      assign sum = a + b;
    endmodule
    ```
  - Example 2: Comparator Module with Internal Logic
    ```
    module comparator(input [3:0] a, input [3:0] b, output greater, equal, less);
      assign greater = a > b;
      assign equal = a == b;
      assign less = a < b;
    endmodule
    ```

- Control Structures:
  - Example 1: Conditional Logic with if-else
    ```
    always @(a or b) begin
      if (a > b)
        max = a;
      else
        max = b;
    end
    ```
  - Example 2: Selecting Options Using case
    ```
    always @(sel) begin
      case (sel)
        2'b00: y = a;
        2'b01: y = b;
        2'b10: y = c;
        2'b11: y = d;
        default: y = 0;
      endcase
    end
    ```

- Operators:
  - Example 1: Arithmetic Operations
    ```
    assign sum = a + b;
    assign difference = a - b;
    ```
  - Example 2: Relational Operators for Comparisons
    ```
    assign isEqual = (a == b);
    assign isGreater = (a > b);
    ```

- Vector and Array Handling:
  - Example 1: Declaring and Using Vectors
    ```verilog
    reg [7:0] data;
    ```
  - Example 2: Operations on Arrays
    ```
    integer array[0:4];
    always @(posedge clk) begin
      array[0] <= 5;
      array[1] <= array[0] + 1;
    end
    ```

- Coding Style:
  - Example 1: Commenting and Code Formatting
    ```
    // This is a simple adder module
    module adder(input a, input b, output sum);
      // Sum is the bitwise OR of a and b
      assign sum = a | b;
    endmodule
    ```
  - Example 2: Naming Conventions and Modular Design
    ```
    module fifo_controller(/* parameters */); // Name clearly indicates purpose
    // ... Module logic ...
    endmodule
    ```

- Common Pitfalls:
  - Example 1: Resolving Inadvertent Latches
    ```
    always @(a or b) begin
      if (a > 0)
        y = b;
      else
        y = y; // Inadvertent latch. Should be `y = 0;` or similar
    end
    ```
  - Example 2: Correct Use of Blocking and Non-blocking Assignments
    ```
    always @(posedge clk) begin
      a <= b; // Non-blocking for sequential logic
      c = a;  // Blocking, but used within the same clock cycle
    end
    ```

