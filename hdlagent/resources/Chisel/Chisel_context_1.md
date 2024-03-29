**User:** Chisel 3.6 Cheatsheet (v0):
--------------------------------------------------------------------------------------
Use Scala val to create wires, instances, etc.
--------------------------------------------------------------------------------------
Instantiate and connect to SubModules
class Parent(n: Int, payloadType: Data) extends Module {
val in = IO(Input(payloadType))
val out = IO(Output(payloadType))
val child = Module(new Delay(n, payloadType))
child.in := in
out := child.out
}
--------------------------------------------------------------------------------------
Casting:
.asTypeOf is hardware cast (works for HW data or Chisel Types)
0.U.asTypeOf(new MyBundle())
chiselTypeOf(...) copy type of HW along with parameters and directions
val foo = IO(chiselTypeOf(bar))
--------------------------------------------------------------------------------------
Standard Library – Stateful:
Counter(n:Int): Counter (simple)
Example:
val c = new Counter(n)
val wrap = WireInit(false.B)
when(cond) { wrap := c.inc() } // .inc returns true when wrap occurs
Counter(cond: UInt, n:Int): (UInt, Bool)
Example:
val countOn = true.B // increment counter every clock cycle
val (counterValue, counterWrap) = Counter(countOn, 4)
when (counterValue === 3.U) {
...
}
Counter(r: Range, enable: Bool, reset: Bool) (UInt, Bool)
Example:
val (counterValue, counterWrap) = Counter(0 until 10 by 2)
when (counterValue === 4.U) {
...
}
LFSR(width: Int, increment: Bool, seed: Option[BigInt]): UInt
Example:
val pseudoRandomNumber = LFSR(16)
ShiftRegister(in: Data, n: Int[, en: Bool]): Data add n registers
Example:
val regDelayTwo = ShiftRegister(nextVal, 2, ena)
--------------------------------------------------------------------------------------
Standard Library – Interfaces.:

Example:
val q = (new Queue(UInt(), 16))
q.io.enq <> producer.io.out
consumer. Module io.in <> q.io .deq
Pipe(enqValid:Bool, enqBits:Data, [latency:Int]) or
Pipe(enq:ValidIO, [latency:Int]): Module delaying input
Interface: io.in: Flipped(ReadyValid[gen]), io.out: ReadyValid[gen]
Example:
val foo = Module(new Pipe(UInt(8.W)), 4)
pipe.io.enq := producer.io
consumer.io := pipe.io.deq
Arbiter(gen: Data, n: Int): Connect multiple producers to one consumer
Interface: io.in Vec of inputs (Flipped(ReadyValid[gen]), io.out: ReadyValid[gen])
Variants: RRArbiter (round robin) LockingArbiter
Example:
val arb = Module(new Arbiter(UInt(), 2))
arb.io.in(0) <> producer0.io.out
consumer.io.in <> arb.io.out
--------------------------------------------------------------------------------------
Definition & Instance:
@instantiable
class Child extends Module {
@public val in = IO(Input(Bool())
@public val out = IO(Output(Bool())
out := in
}
class Parent(n: Int, payloadType: Data) extends Module {
val childDef = Definition(new Delay(n, payloadType))
val in = IO(Input(payloadType))
val out = IO(Output(payloadType))
val child = Instance(childDef)
child.in := in
out := child.out
}

Note: To use some of the Standard Library operators such as Fill() and Cat(), or bit checks such as Mux(), Mux1H(), MuxLookup(), MuxCase(), and PopCount, you must add the following line to the Chisel code to import these features: ```import chisel3.util._```
