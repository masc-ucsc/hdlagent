# Chisel Language Reference Guide for LLMs

This guide provides a concise reference for generating Chisel code, focusing on unique aspects and syntax of the Chisel Hardware Description Language (HDL). It includes code snippets and explanations of key concepts that differ from traditional HDLs.

## Type Conversions

### Creating UInt from a Bundle

To convert a `Bundle` instance to `UInt`, use the `asUInt` method.

```scala
class MyBundle extends Bundle {
  val foo = UInt(4.W)
  val bar = UInt(4.W)
}

class Foo extends Module {
  val bundle = Wire(new MyBundle)
  bundle.foo := 0xc.U
  bundle.bar := 0x3.U
  val uint = bundle.asUInt
  printf(cf"$uint") // 195
}
```

### Creating Bundle from a UInt

To reinterpret a `UInt` as a `Bundle`, use the `asTypeOf` method.

```scala
class MyBundle extends Bundle {
  val foo = UInt(4.W)
  val bar = UInt(4.W)
}

class Foo extends Module {
  val uint = 0xb4.U
  val bundle = uint.asTypeOf(new MyBundle)
  printf(cf"$bundle") // Bundle(foo -> 11, bar -> 4)
}
```

### Tying off a Bundle/Vec to 0

Use `asTypeOf` with `0.U` or `chiselTypeOf` for dynamic types.

```scala
class MyBundle extends Bundle {
  val foo = UInt(4.W)
  val bar = Vec(4, UInt(1.W))
}

class Foo(typ: MyBundle) extends Module {
  val bundleA = IO(Output(typ))
  bundleA := 0.U.asTypeOf(typ)
}
```

### Creating Vec of Bools from a UInt

Use `VecInit` with `asBools` method.

```scala
class Foo extends Module {
  val uint = 0xc.U
  val vec = VecInit(uint.asBools)
  printf(cf"$vec") // Vec(0, 0, 1, 1)
}
```

### Creating UInt from a Vec of Bool

Convert a `Vec[Bool]` to `UInt` using `asUInt`.

```scala
class Foo extends Module {
  val vec = VecInit(true.B, false.B, true.B, true.B)
  val uint = vec.asUInt
  printf(cf"$uint") // 13
}
```

## Vectors and Registers

### 2D or 3D Vectors

Use `VecInit.fill` or `VecInit.tabulate` for multi-dimensional Vectors.

```scala
class Foo extends Module {
  val twoDVec = VecInit.fill(2, 3)(5.U)
  val threeDVec = VecInit.fill(1, 2, 3)(myBundle)
}
```

### Vector of Registers

Prefer `Reg(Vec(...))` over `Vec(Reg(...))`.

```scala
class Foo extends Module {
  val regOfVec = Reg(Vec(4, UInt(32.W)))
  regOfVec(0) := 123.U
}
```

## Bundles

### Aliased Bundle Fields

To avoid aliased fields in Bundles, use function parameters or by-name parameters.

```scala
class UsingAFunctionBundle[T <: Data](gen: () => T) extends Bundle {
  val foo = gen()
  val bar = gen()
}
```

## Finite State Machines (FSM)

Use `ChiselEnum` for state definitions and `switch`/`is` for state transitions.

```scala
object State extends ChiselEnum {
  val sNone, sOne1, sTwo1s = Value
}

class DetectTwoOnes extends Module {
  val state = RegInit(State.sNone)
  switch (state) {
    is (State.sNone) { /* ... */ }
  }
}
```

## Unpacking and Subword Assignment

### Unpacking a Value

Reinterpret a `UInt` as a structured type using `asTypeOf`.

```scala
class Foo extends Module {
  val z = Wire(UInt(9.W))
  val unpacked = z.asTypeOf(new MyBundle)
}
```

### Subword Assignment

Chisel does not support direct subword assignment. Use `VecInit` for bit manipulation.

```scala
class Foo extends Module {
  val bools = VecInit(io.in.asBools)
  bools(0) := io.bit
  io.out := bools.asUInt
}
```

## Optional I/O

Use `Option` for optional I/O ports.

```scala
class ModuleWithOptionalIOs(flag: Boolean) extends Module {
  val io = IO(new Bundle {
    val out2 = if (flag) Some(Output(UInt(12.W))) else None
  })
}
```

## Predictable Naming

Override `desiredName` for custom module names.

```scala
class Coffee extends BlackBox {
  override def desiredName = "Tea"
}
```

## Directionality

To override directionality within a module, use `withClock`, `withReset`, or mixin traits like `ImplicitClock`.

```scala
class MyModule extends Module with ImplicitClock {
  override protected def implicitClock = gatedClock
}
```

This guide should assist LLMs in generating accurate and idiomatic Chisel code, focusing on aspects that differ from traditional HDLs.
