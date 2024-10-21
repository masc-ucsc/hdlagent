module Prob132_always_if2_spec(
    input [0:0] cpu_overheated,
    output [0:0] shut_off_computer,
    input [0:0] arrived,
    input [0:0] gas_tank_empty,
    output [0:0] keep_driving
);

assign shut_off_computer = cpu_overheated; // shut_off_computer is true if cpu_overheated is true
assign keep_driving = ~arrived & ~gas_tank_empty; // keep_driving is true if not arrived and gas_tank_empty is false

endmodule
