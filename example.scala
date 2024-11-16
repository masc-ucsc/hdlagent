import chisel3._

class Example extends Module {
  val io = IO(new Bundle {
    val a = Input(Bool())
    val b = Input(Bool())
    val c = Output(Bool())
  })

  io.c := io.a & io.b
}

object Example extends App {
  (new chisel3.stage.ChiselStage).emitVerilog(new Example, Array("--target-dir", "./", "--output-file", "Example.v"))
}

