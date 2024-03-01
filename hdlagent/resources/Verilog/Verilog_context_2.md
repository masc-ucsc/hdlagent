**User:**
Title: Sequential Logic in Verilog

- Edge Detection: Implementing detectors for signal edges.
  - Example 1: `always @(posedge clock) if (prev_signal && !signal) detected <= 1;` (Rising edge)
  - Example 2: `always @(posedge clock) if (!prev_signal && signal) detected <= 1;` (Falling edge)
- Synchronous and Asynchronous Resets: Discussing reset mechanisms in sequential designs.
  - Example 1: `always @(posedge clock or negedge reset) if (!reset) Q <= 0; else Q <= D;` (Asynchronous reset)
  - Example 2: `always @(posedge clock) if (reset) Q <= 0; else Q <= D;` (Synchronous reset)
- Metastability and Synchronization: Explaining issues and solutions in multi-clock domain designs.
  - Example 1: Two-flip-flop synchronizer.
- Clock Dividers: How to create clock dividers.
  - Example 1: Dividing clock frequency.
  - Example 2: Generating different clock phases.

- Simple Control Structures:
  - Conditional Statements: `if`, `else`.
    - Example: `if (a > b) ... else ...`
  - Loops: Mainly used in testbenches (`for`, `while`).
    - Example: `for (i = 0; i < limit; i = i + 1) ...`
- Variable Scope:
  - Local vs. Global Variables: Module-level (global) vs. block-level (local).
    - Example: `module myMod; reg a; ... endmodule`
  - Variable Visibility and Lifetime: Depends on where it's declared.
    - Example: Inside a module vs. inside a block.

