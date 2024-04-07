#
 Chisel Tutorial: The Basics

## Introduction

Chisel is a hardware construction
 language developed at UC Berkeley. This tutorial will teach you the basics of the language
 by building a simple 8-bit adder. For more information, see the Chisel website [here](https://chisel.eecs.berkeley.
edu/).

## Getting Started

To get started with Chisel, you will need to install the following:

* Java 8 or later
* S
BT
* A text editor or IDE (e.g., VSCode, IntelliJ)

Once you have installed the required software, you can create a new Chisel project by running the following command in a terminal:

```
s
bt new chisel-template.g8
```

This will create a new directory called "adder" containing a basic Chisel project.

## Writing Your First Chisel Module

To write your first Chisel module, open the file
 "adder/src/main/scala/Adder.scala" in your text editor or IDE. This file contains the following code:

```scala
import chisel3._

class Adder extends Module {
  val io = IO(new Bundle {
    val in1 = Input(UInt(8.W
))
    val in2 = Input(UInt(8.W))
    val out = Output(UInt(8.W))
  })

  io.out := io.in1 + io.in2
}
```

This code defines a simple 8-bit adder. The `
Adder` class extends the `Module` class, which is the base class for all Chisel modules. The `io` field defines the input and output ports of the module. In this case, the adder has two input ports (`in1` and `in2`) and one output port (`out`). Each port
 is defined with a type and a width. For example, `in1` is an 8-bit unsigned integer (`UInt(8.W)`).

The `:=` operator is used to connect the input ports to the output port. In this case, the `out` port is connected to the sum
 of the `in1` and `in2` ports.

## Building and Running Your Module

To build and run your Chisel module, run the following commands in a terminal:

```
sbt compile
sbt run
```

This will compile your module and generate a Verilog file. The
 Verilog file can then be simulated using a simulator such as Icarus Verilog.

## Conclusion

This tutorial has covered the basics of Chisel. For more information, please refer to the Chisel website [here](https://chisel.eecs.berkeley.edu/).
