##
 Chisel Reference Syntaxes, Data Types, and Core Concepts

### Value Declaration

```ch
Int width = 8
UInt x = UInt(width
.W) // 8-bit unsigned integer
Bool y = Bool() // 1-bit boolean
```

### Bundle Declaration
```ch

import chisel3._
import chisel3.experimental.BundleLiterals._
class MyBundle extends Bundle {
  val foo = UInt(8.W)

  val bar = UInt(8.W)
  val myLiteral = MyCustomLiteral() // Your custom literal object here
}
```

### Module Interface (IO) Declaration
```ch
val io = IO(
new Bundle {
    val in = Input(UInt(8.W))
    val out = Output(UInt(8.W))
  })
```

### Clock and Reset
```ch
val clock = Input(
Clock())
val reset = Input(Bool())
```

### Assignment
```ch
out := in
```

### Arithmetic and Logic
```ch
val add = in1 + in2
val sub = in1 - in2
val and = in1 & in2
val or = in
1 | in2
```

### Comparison
```ch
val eq = in1 === in2
val ne = in1 =/= in2
val lt = in1 < in2
```

### Conditional Statements
```ch
if (cond) {
    // Statements
}
when (
cond) {
    // Statements
}
```

### Loops
```ch
for (i <- 0 until 10) {
    // Loop statements
}
```

### Registers
```ch
val reg = RegInit(UInt(8.W), 0.U)

val vecReg = RegInit(Vec(4, UInt(8.W)), VecInit(Seq(0.U, 0.U, 0.U, 0.U)))
```

### Wires
```ch
val wire = Wire(UInt(8.W))
```


### Vectors
```ch
val vec = Vec(4, UInt(8.W))
```

### Modules
```ch
class MyModule extends Module {
    val io = IO(new Bundle {
        val in = Input(UInt(8.W))
        val out = Output(
UInt(8.W))
    })
    out := in
}
```

### Key Chisel Differences:

- Accessing bundle fields without `.get`: `bundle.foo` instead of `bundle.getFoo()`.
- No setter methods for fields: `bundle.foo := 1
` instead of `bundle.setFoo(1)`.
- Different I/O syntax: `val io = IO(...)` instead of `val io = new IOBundle(...)`.
- No need to declare Chisel types before using them: `UInt(8.W)` instead of `Data.
uint(8)`.
- No need to declare module inputs and outputs before using them: `val in = Input(UInt(8.W))` instead of `val in = in.UInt(8)`.
- Different module class syntax: `class MyModule extends Module` instead of `object My
Module extends Module`.
- No need to call `elaborate()` or `compile()` explicitly: Chisel will automatically elaborate and compile the design when it is instantiated.
