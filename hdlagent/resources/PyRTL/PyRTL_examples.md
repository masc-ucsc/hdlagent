**User:** Write me a pyrtl program named 'nor_reduction' that takes a 8-bit input 'bus_i' and has a 1-bit output 'reduce_o' which is the NOR reduction of 'bus_i'.

**Assistant:** ```
import pyrtl

bus_i = pyrtl.wire.Input(8, 'bus_i')  # 8 bit input, READ-ONLY
reduce_o = pyrtl.wire.Output(1, 'reduce_o')     # 1 bit output, WRITE-ONLY

# pyrtl has unary reduction methods: 'pyrtl.corecircuits.and_all_bits()', 'pyrtl.corecircuits.or_all_bits()', and 'pyrtl.coreciruits.xor_all_bits()'
reduce_o <<= ~pyrtl.corecircuits.or_all_bits(bus_i)    # '<<=' is how wires are driven by already existing wires, equivalent to 'assign' in Verilog

with open ('nor_reduction_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset=False)
```

**User:** Write me a pyrtl program named 'odds_evens_sum' that takes a 7-bit input 'in_i' and has three outputs. 'odds_o' is 3-bits wide and is the odd-numbered bits from the input, concatenated in order. Conversely, 'evens_o' is 4-bits wide and is the even-numbered bits. The last output 'sum_o' is the 5-bit wide sum of 'odds_o' and 'evens_o'.

**Assistant:** ```
import pyrtl

in_i = pyrtl.wire.Input(7, 'in_i')           # 7 bit input, READ-ONLY
odds_o = pyrtl.wire.Output(3, 'odds_o')      # 3 bit output, WRITE-ONLY
evens_o = pyrtl.wire.Output(4, 'evens_o')    # 4 bit output, WRITE-ONLY
sum_o = pyrtl.wire.Output(5, 'sum_o')        # 5 bit output, WRITE-ONLY

# Outputs are write-only, so intermediate values are created when needed elsewhere
odds_wire = pyrtl.corecircuits.concat(in_i[5], in_i[3], in_i[1])
# Drive the output with intermediate value
odds_o <<= odds_wire

# 'pyrtl.corecircuits.concat()' is the concatenation operator
evens_wire = pyrtl.corecircuits.concat(in_i[6], in_i[4], in_i[2], in_i[0])
evens_o <<= evens_wire

# bitwidth extensions are done by 'sign_extended()' and 'zero_extended()'
odds_sign_ext = odds_wire.zero_extended(4)
# addition bitwidth is the max width of the two operands + 1
sum_o <<= evens_wire + odds_sign_ext

with open('odds_evens_sum_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset=False)
```

**User:** Write me a pyrtl program named 'simple_alu' that implements an Arithmetic Logic Unit which has three inputs: 'rs1_i' and 'rs2_i' are both 8-bit wide value inputs, and 'op_i' is a 2-bit wide opcode input, which determines the operation performed on 'rs1_i' and 'rs2_i'. The function has a single 8-bit output 'result_o', which is set to the sum of the inputs when the opcode is 0, the difference of the inputs when the opcode is 1, and the product of the inputs when the opcode is 2. No other operations are supported, so if an unknown opcode is detected, the output is set to zero.

**Assistant:** ```
import pyrtl

rs1_i = pyrtl.wire.Input(8, 'rs1_i')
rs2_i = pyrtl.wire.Input(8, 'rs2_i')
op_i = pyrtl.wire.Input(2, 'op_i')
result_o = pyrtl.wire.Output(8, 'result_o')

# Verilog-style constant declaration
ADD = 0b00
SUB = 0b01
MUL = 0b10

# pyrtl does not have 'case/switch', instead must use 'with pyrtl.conditional_assignment'
# another simple conditional is 'pyrtl.mux()'
with pyrtl.conditional_assignment:
    with op_i == ADD:
        result_o |= rs1_i + rs2_i    # conditional wire drive is '|=' reserved ONLY for 'with' blocks
    with op_i == SUB:
        result_o |= rs1_i - rs2_i    # all operations result truncated to 8 bits by result_o wire declaration
    with op_i == MUL:                # multiplication result width is 2 * max bitwidth of operands
        result_o |= rs1_i * rs2_i
    with pyrtl.otherwise:            # default/else statement handled by 'pyrtl.otherwise'
        result_o |= 0

with open('simple_alu_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset=False)
```

**User:** Write me a pyrtl function that uses a compile loop to add up the values from 7 to 11. The name should be 'add_7_to_11' and has 16-bit output 'res_o'

**Assistant:** ```
import pyrtl

res_o = pyrtl.wire.Output(16, 'res_o')
res_o <<= sum(range(7, 12))  # Python computation can be used to assist with pyrtl 

with open('add_7_to_11.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset=False)
``` 

**User:** Write me a PyRTL function that is a naive implementation of the RISC-V FMAdd instruction, where the opcode is as listed in the official spec, but any FP rules are ignored as well as the RM and FMT fields. The source operands will take on the values of their register numbers. The 'result' output will be the multiply-add operation, and the 'rd' output will be the decoded destination register. If the opcode is incorrect, then the 'err' output must be set and the other outputs must be cleared. The equivalent Verilog declaration would be 'module fmadd(input [31:0] instruction, output [4:0] rd, output [31:0] result, output err);'

**Assistant:** ```
import pyrtl

instruction = pyrtl.wire.Input(32, 'instruction')
rd = pyrtl.wire.Output(5, 'rd')
result = pyrtl.wire.Output(32, 'result')
err = pyrtl.wire.Output(1, 'err')

FMADD_OPCODE = 0b1000011

opcode = instruction[0:7]   # Python part select, extract bits 0 to 6

rs1 = instruction[15:20]    # bits 15 to 19
rs2 = instruction[20:25]    # bits 20 to 24
rs3 = instruction[27:32]    # bits 27 to 31

with pyrtl.conditional_assignment:
    with opcode == FMADD_OPCODE:
        rd |= instruction[7:12]     # only explicitly declared wires, like 'Input', 'Output', or 'WireVector' can be driven
        result |= (rs1 * rs2) + rs3 # ONLY use conditional drive '|=' in 'with' blocks
        err |= 0
    with pyrtl.otherwise:
        rd |= 0
        result |= 0
        err |= 1

with open('fmadd_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset=False)
```

**User:** Write me a PyRTL function that is a 1 stage pipelined adder, this means the result should be updated within 1 clock cycle. The carry out bit should be preserved in the extended output. The reset should be asynchronous, and the reset value should be 0. The equivalent Verilog declaration would be 'module async_adder (input clk, input rst, input [1:0] a, input [1:0] b, output [2:0] result );'

**Assistant:** ```
import pyrtl

# reset and clock signals are implicit, AVOID explicit declaration
a = pyrtl.wire.Input(2, 'a')
b = pyrtl.wire.Input(2, 'b')
result = pyrtl.wire.Output(3, 'result')

# Initialize state Register, bitwidth 3, reset value 0
result_reg = pyrtl.wire.Register(3, 'result_reg', 0)

# Non-blocking assignment of next value for Register to capture
result_reg.next <<= a + b

# Connect register to output
result <<= result_reg

with open('async_adder_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f, add_reset='asynchronous') # make reset asynchronous with 'add_reset='asynchronous''
```

**User:** Write me a PyRTL function that implements a Finite State Machine (FSM) simulating the game "green light, red light". The purpose of the game is to be in the 'GO_STATE' (state value 1) as soon as the 'GREEN_IN' signal (input value 1) is received, and to stay in that state until the 'RED_IN' signal (input value 0) is received. The state should then transition to 'STOP_STATE' (state value 0) and stay there until the 'GREEN_IN' signal is received again. The input to the class is the signal, and the output is the current state. The default/reset state should be 'STOP_STATE' and the reset is synchronous. The circuit has only one pipeline stage, meaning the result is updated on the next clock cycle. The reset value should be 0. The equivalent Verilog declaration would be 'module stoplight_fsm (input clk, input rst, input signal_i, output state_o);'.

**Assistant:** ```
import pyrtl

# reset and clock signals are implicit, AVOID explicit declaration
signal_i = pyrtl.wire.Input(1, 'signal_i')
state_o = pyrtl.wire.Output(1, 'state_o')

# Initialize state Register, bitwidth 1, reset value 0
state_r = pyrtl.wire.Register(1, 'state_r', 0)

# Verilog-style constant declaration
# Define FSM states
STOP_STATE = 0b0
GO_STATE = 0b1
# Define FSM inputs
RED_IN = 0b0
GREEN_IN = 0b1

# pyrtl does not have 'case/switch', instead must use 'with pyrtl.conditional_assignment', can also use 'pyrtl.corecircuits.mux()'
with pyrtl.conditional_assignment:
    with state_r == STOP_STATE:
        state_r.next |= pyrtl.corecircuits.mux(signal_i == GREEN_IN, state_r, GO_STATE)    # when in 'STOP_STATE', change to 'GO_STATE' upon first 'GREEN_IN', otherwise maintain state
    with state_r == GO_STATE:
        state_r.next |= pyrtl.corecircuits.mux(signal_i == RED_IN, state_r, STOP_STATE)      # when in 'GO_STATE', change to 'STOP_STATE' upon first 'RED_IN', otherwise maintain state
    with pyrtl.otherwise:            # default/else statement handled by 'pyrtl.otherwise'
        state_r.next |= STOP_STATE   # conditional wire drive is '|=' reserved ONLY for 'with' blocks

# Connect register to output
state_o <<= state_r

with open('stoplight_fsm_pyrtl.v', 'w') as f:
    pyrtl.output_to_verilog(f)
```
