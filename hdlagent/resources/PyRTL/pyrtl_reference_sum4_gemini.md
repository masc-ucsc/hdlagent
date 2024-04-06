##
 Syntax Differences between PyRTL and other HDLs

| Feature | PyRTL |
 Other HDLs |
|---|---|---|
| WireVector | `WireVector
(bitwidth=None, name='', block=None)` | `wire` |
| Logic | `a + b` | `a or b`
 |
| Or | `a | b` | `a & b` |
| And | `a & b` | `a xor b`
 |
| Xor | `a ^ b` | `~a` |
| Not | `~a` | `a << b` |
| Shift Left | `a << b` | `a >> b`
 |
| Shift Right | `a >> b` | `==` |
| Equality | `a == b` | `!=` |
| Not Equal | `a != b` | `<` |
| Less Than
 | `a < b` | `>` |
| Greater Than | `a > b` | `<=` |
| Less or Equal to | `a <= b` | `>=` |
| Greater or Equal to | `a >= b` | `:=` |
| Assignment | `
a <<= b` | `always @(posedge clk) begin` |
| Conditional Assignment | `with conditional_assignment:` | `if else` |
| Bitwise NAND | `a nand b` | `case` |
| Bitwise NOR | `a nor b` | `default` |

| Case Statement | `with case sel:` | `for` |
| For Loop | `with for var in range(min, max)` | `while` |
| While Loop | `with while cond:` | `RAM` |
| Memory | `memory[address]` | `FIFO` |

| FIFO | `fifo.read` | `ROM` |
| ROM | `rom[address]` | |
| Input Pins | `Input(bitwidth=None, name='', block=None)` | |
| Output Pins | `Output(bitwidth=None, name='', block=None
)` | |
| Constants | `Const(val, bitwidth=None, name='', signed=False, block=None)` | |
| Conditionals | `conditional_assignment` | |
