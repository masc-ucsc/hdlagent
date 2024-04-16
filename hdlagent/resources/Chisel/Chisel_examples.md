**User:** Write me a Chisel class named 'nor_reduction' that takes a 8-bit input 'bus_i' and has a 1-bit output 'reduce_o' which is the NOR reduction of 'bus_i'.

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class nor_reduction extends Module {
  val io = IO(new Bundle {
  val bus_i = Input(UInt(8.W))
  val out = Output(UInt(1.W))
})
    // available reduction methods are '.andR', '.orR', and 'xorR'
    io.out := !io.bus_i.orR     // ':=' is how wires and registers are driven
}
```

**User:** Write me a Chisel class named 'odds_evens_sum' that takes a 7-bit input 'in_i' and has three outputs. 'odds_o' is 3-bits wide and is the odd-numbered bits from the input, concatenated in order. Conversely, 'evens_o' is 4-bits wide and is the even-numbered bits. The last output 'sum_o' is the 5-bit wide sum of 'odds_o' and 'evens_o'.

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class odds_evens_sum extends Module {
  val io = IO(new Bundle {
  val in_i = Input(UInt(7.W))
  val odds_o = Output(UInt(3.W))
  val evens_o = Output(UInt(4.W))
  val sum_o = Output(UInt(5.W))
})
    // 'Cat()' is the concatenation operator
    io.odds_o := Cat(io.in_i(5), io.in_i(3), io.in_i(1))     // Extraction bit-select bits 5, 3, 1
    io.evens_o := Cat(io.in_i(6), io.in_i(4), io.in_i(2), io.in_i(0))  //  bit select bits 6, 4, 2, 0

    // Intermediate values (wires) created with 'val' keyword
    val odds_zext_wire = Wire(UInt(5.W))
    // Zero extends 3-bit odds_o to 5-bits. Sign extend happens when a 'val' is declared with 'SInt(N.W)'
    odds_zext_wire := io.odds_o

    val evens_zext_wire = Wire(UInt(5.W))
    evens_zext_wire := io.evens_o

    // 'asUInt(N.W)' typecasts and zero extends, 'asSInt(N.W)' typecasts and sign extends
    io.sum_o := odds_zext_wire + evens_zext_wire  // output bitwidth of addition is max of bitwidths of operands
}
```

**User:** Write me a Chisel class named 'simple_alu' that implements an Arithmetic Logic Unit which has three inputs: 'rs1_i' and 'rs2_i' are both 8-bit wide value inputs, and 'op_i' is a 2-bit wide opcode input, which determines the operation performed on 'rs1_i' and 'rs2_i'. The function has a single 8-bit output 'result_o', which is set to the sum of the inputs when the opcode is 0, the difference of the inputs when the opcode is 1, and the product of the inputs when the opcode is 2. No other operations are supported, so if an unknown opcode is detected, the output is set to zero.

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class simple_alu extends Module {
  val io = IO(new Bundle {
  val rs1_i = Input(UInt(8.W))
  val rs2_i = Input(UInt(8.W))
  val op_i = Input(UInt(2.W))
  val result_o = Output(UInt(8.W))
})
    val ADD = 0.U(2.W)  // value 0 constant, 2 bit wide
    val SUB = 1.U(2.W)  // value 1 constant, 2 bit wide
    val MUL = 2.U(2.W)  // value 2 constant, 2 bit wide

    // default value
    io.result_o := 0.U(2.W)
    // case/switch statement, conditionally modifies 'io.result_o' if case match found
    switch(io.op_i) {
      is(ADD) { io.result_o := io.rs1_i + io.rs2_i }
      is(SUB) { io.result_o := io.rs1_i - io.rs2_i }
      is(MUL) { io.result_o := io.rs1_i * io.rs2_i }  // truncated output width, multiplication width is the sum of the operands' widths
    }
}
```

**User:** Write me a Chisel class that uses a compile loop to add up the values from 7 to 11. The name should be 'add_7_to_11' and has 16-bit output 'res_o'

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class add_7_to_11 extends Module {
  val io = IO(new Bundle {
  val res_o = Output(UInt(16.W))
})

    // Accumulate a constant value using a Scala for loop
    var accumulator = 0
    for (i <- 7 to 11) {
      accumulator += i
    }

    // Use the accumulated value as a constant in your hardware
    val accumulatedValue: UInt = accumulator.U
    io.res_o := accumulatedValue
}
``` 

**User:** Write me a Chisel class that is a naive implementation of the RISC-V FMAdd instruction, where the opcode is as listed in the official spec, but any FP rules are ignored as well as the RM and FMT fields. The source operands will take on the values of their register numbers. The 'result' output will be the multiply-add operation, and the 'rd' output will be the decoded destination register. If the opcode is incorrect, then the 'err' output must be set and the other outputs must be cleared. The equivalent Verilog declaration would be 'module fmadd(input [31:0] instruction, output [4:0] rd, output [31:0] result, output err);'

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class fmadd extends Module {
  val io = IO(new Bundle {
  val instruction = Input(UInt(32.W))
  val rd = Output(UInt(5.W))
  val result = Output(UInt(32.W))
  val err = Output(Bool())
})
    // const declaration, explicit width
    val FMADD_OPCODE = "b1000011".U(7.W)

    // implicit width declarations, inferred by compiler
    val rs1 = io.instruction(19, 15)  // extract bits 15 to 19
    val rs2 = io.instruction(24, 20)  // extract bits 20 to 24
    val rs3 = io.instruction(31, 27)  // extract bits 27 to 31
    val rd = io.instruction(11, 7)    // extract bits 7 to 11
    val opcode = io.instruction(6, 0)

    // Zero extend operations to 32 bits
    val product = Wire(UInt(32.W))
    val sum = Wire(UInt(32.W))
    product := rs1 * rs2
    sum := product + rs3

    io.err := FMADD_OPCODE =/= opcode

    // 'Mux()' used as ternay operator, can also be nested. Requires 'Bool' type, can typecast '.asBool' when needed
    io.rd := Mux(io.err, 0.U(5.W), rd)
    io.result := Mux(io.err, 0.U(32.W), sum)
}
```

**User:** Write me a Chisel class that implements a Finite State Machine (FSM) simulating the game "green light, red light". The purpose of the game is to be in the 'GO_STATE' (state value 1) as soon as the 'GREEN_IN' signal (input value 1) is received, and to stay in that state until the 'RED_IN' signal (input value 0) is received. The state should then transition to 'STOP_STATE' (state value 0) and stay there until the 'GREEN_IN' signal is received again. The input to the class is the signal, and the output is the current state. The default/reset state should be 'STOP_STATE' and the reset is synchronous. The circuit has only one pipeline stage, meaning the result is updated on the next clock cycle. The reset value should be 0. The equivalent Verilog declaration would be 'module stoplight_fsm (input clk, input rst, input signal_i, output state_o);'.

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

// clock and reset are implicitly declared, AVOID explicit declaration
class stoplight_fsm extends Module {
  val io = IO(new Bundle {
  val signal_i = Input(UInt(1.W))
  val state_o = Output(UInt(1.W))
})

    // Initialize state Register 1 bit wide, reset value 0, set by '0.U(1.W)'
    val state_r = RegInit(0.U(1.W))
    // Define FSM states
    val STOP_STATE = 0.U(1.W)
    val GO_STATE = 1.U(1.W)
    // Define FSM inputs
    val RED_IN = 0.U(1.W)
    val GREEN_IN = 1.U(1.W)

    // default state
    state_r := STOP_STATE
    // case/switch statement, FSM logic
    switch(state_r) {
      is(STOP_STATE) { state_r := Mux(io.signal_i === GREEN_IN, GO_STATE, state_r) } // when in 'STOP_STATE', change to 'GO_STATE' upon first 'GREEN_IN', otherwise maintain state
      is(GO_STATE)   { state_r := Mux(io.signal_i === RED_IN, STOP_STATE, state_r) } // when in 'GO_STATE', change to 'STOP_STATE' upon first 'RED_IN', otherwise maintain state
    }

    io.state_o := state_r
}
```

**User:** Write me a Chisel class that is a 1 stage pipelined adder, this means the result should be updated within 1 clock cycle. The carry out bit should be preserved in the extended output. The reset should be asynchronous, and the reset value should be 0. The equivalent Verilog declaration would be 'module async_adder (input clk, input rst, input [1:0] a, input [1:0] b, output [2:0] result );'

**Assistant:** ```
import chisel3._
import chisel3.util._   // imports standard library

class async_adder extends Module with RequireAsyncReset {   // 'with RequireAsyncReset' enforces asycnronous reset on implicit reset signal
  val io = IO(new Bundle {                                  // Clock and Reset signals implicitly declared, AVOID explicit delcaration
  val a = Input(UInt(2.W))
  val b = Input(UInt(2.W))
  val result = Output(UInt(3.W))
})
    // Extend inputs to 3 bits to preserve carry-out bit
    val a_zero_ext = Wire(UInt(3.W))
    val b_zero_ext = Wire(UInt(3.W))
    a_zero_ext := io.a
    b_zero_ext := io.b

    // Initialize Register, 3-bit wide set by '3.W', default reset value is 0. set by '0.U'
    val result_reg = RegInit(0.U(3.W))
    // Connect adder to Register just like a Wire
    result_reg := a_zero_ext + b_zero_ext
    io.result := result_reg
}
```
