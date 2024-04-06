**
WireVector**

* A WireVector is a hardware description language with the following
 reference documentation and tutorial.
* WireVectors act much like a list of wires
, except that there is no “contained” type, each slice of a WireVector is itself a WireVector (even if just a single “bit” of
 information).
* The least significant bit of the wire is at index 0 and normal list slicing syntax applies (i.e. "myvector[0
:5]" makes a new vector from the bottom 5 bits of "myvector", "myvector[-1]" takes the most significant bit, and "myvector[-4:]" takes the 4 most significant bits).

**
Logic**

**Wires and Logic**

* Wires define the relationship between logic blocks in PyRTL. They are treated like normal wires in traditional RTL systems except the "Register" wire.
* Logic is then created when wires are
 combined with one another using the provided operators.
* For example, if "a" and "b" are both of type "WireVector", then "a + b" will make an adder, plugs "a" and "b" into the inputs of that adder, and return a new "WireVector"
 which is the output of that adder.
* "Block" stores the description of the hardware as you build it.

**WireVector**

**Mathematical Operations**

* WireVectors act much like a list of wires, except that there is no “contained” type, each slice of a WireVector is itself
 a WireVector (even if just a single “bit” of information).
* The least significant bit of the wire is at index 0 and normal list slicing syntax applies (i.e. "myvector[0:5]" makes a new vector from the bottom 5 bits of "myvector", "
myvector[-1]" takes the most significant bit, and "myvector[-4:]" takes the 4 most significant bits).

**Input, Output, Const, and Register**

* Input, Output, Const, and Register all derive from WireVector.
* Input represents an input pin, serving as
 a placeholder for an external value provided during simulation.
* Output represents an output pin, which does not drive any wires in the design.
* Const is useful for specifying hard-wired values and
* Register is how sequential elements are created (they all have an implicit clock).

**Blocks and Logic Nets**


* Blocks define the hardware as you build it.
* LogicNets define the basic immutable datatype for storing a “net” in a netlist.
* A ‘net’ is a structure in Python that is representative of hardware logic operations. These include binary operations, such as *and* *or* and
 *not*, arithmetic operations such as *+* and *-*, as well as other operations such as Memory ops, and concat, split, wire, and reg logic.

**Helper Functions**

* Helper functions provide ways of combining, slicing, and extending "WireVectors" in ways that are often useful in hardware design
.
* The functions below extend those member functions of the "WireVector" class itself (which provides support for the Python builtin "len", slicing e.g. "wire[3:6]", "zero_extended()", "sign_extended()", and many operators such as addition and multiplication).

**Cutting and
 Extending WireVectors**

* The functions below provide ways of combining, slicing, and extending "WireVectors" in ways that are often useful in hardware design.
* The functions below extend those member functions of the "WireVector" class itself (which provides support for the Python builtin "len", slicing e.g
. "wire[3:6]", "zero_extended()", "sign_extended()", and many operators such as addition and multiplication).

**Coercion to WireVector**

* There is only one function in PyRTL in charge of coercing values into "WireVectors", and that is "as_wires
()".
* This function is called in almost all helper functions and classes to manage the mixture of constants and WireVectors that naturally occur in hardware development.

**Control Flow Hardware**

**Mux**

* Multiplexer returning the value of the wire from *mux_ins* according to *index*.

**
Select**

* Multiplexer returning *falsecase* when "sel == 0", otherwise *truecase*.

**Enum Mux**

* Build a mux for the control signals specified by an enum.

**Bitfield Update**

* Return WireVector *w* but with some of the bits
 overwritten by *newvalue*.

**Bitfield Update Set**

* Return WireVector *w* but with some of the bits overwritten by values in *update_set*.

**Match Bitpattern**

* Returns a single-bit WireVector that is 1 if and only if *w* matches the
 *bitpattern*, and a tuple containing the matched fields, if any. Compatible with the *with* statement.

**Creating Lists of WireVectors**

* Allocate and return a list of "Inputs".
* Allocate and return a list of "Outputs".
* Allocate and return a list of "Registers".

* Allocate and return a list of WireVectors.

**Interpreting Vectors of Bits**

* Return value as intrepreted as a signed integer under two’s complement.
* Return a string representation of the value given format specified.
* Return an unsigned integer representation of the data given format specified.


**Inferring Value and Bitwidth**

* Return a tuple (value, bitwidth) infered from the specified input.

**Logging**

* Set the global debug mode.
* Print useful information about a WireVector when in debug mode.
* Add hardware assertions to be checked on the RTL
 design.

**Reductions**

* Returns WireVector, the result of “and”ing all items of the argument vector.
* Returns WireVector, the result of “or”ing all items of the argument vector.
* Returns WireVector, the result of “xor”ing all items of the
 argument vector.

**Extended Logic and Arithmetic**

* The functions below provide ways of comparing and arithmetically combining "WireVectors" in ways that are often useful in hardware design.
* The functions below extend those member functions of the "WireVector" class itself (which provides support for addition, unsigned multiplication
, unsigned comparison, and many others).

**Registers and Memories**

**Registers**

* The class "Register" is derived from "WireVector", and so can be used just like any other "WireVector".
* Reading a register produces the stored value available in the current cycle. The stored value for
 the following cycle can be set by assigning to property "next" with the "<<=" ("__ilshift__()") operator.

**Memories**

* MemBlock is the object for specifying block memories.
* It can be indexed like an array for both reading and writing.
* Writes under a conditional are automatically
 converted to enabled writes.

**ROMs**

* PyRTL Read Only Memory.
* They support the same read interface and normal memories, but they are cannot be written to (i.e. there are no write ports).
