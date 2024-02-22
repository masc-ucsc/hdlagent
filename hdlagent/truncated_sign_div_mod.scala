import chisel3._
import chisel3.util._

class truncated_sign_div_mod extends Module {
  val io = IO(new Bundle {
    val a = Input(SInt(8.W))
    val b = Input(SInt(8.W))
    val div = Output(SInt(6.W))
    val mod = Output(SInt(6.W))
  })

  when(io.b === 0.S) {
    // Division by zero is unspecified, setting to zero
    io.div := 0.S
    io.mod := 0.S
  } .otherwise {
    val divFull = io.a / io.b
    val modFull = io.a % io.b
    // Saturate the result to 6 bits
    io.div := divFull.head(8).tail(2).asSInt
    io.mod := modFull.head(8).tail(2).asSInt
  }
}