module TopModule(
    input ring,
    input vibrate_mode,
    output ringer,
    output motor
);

// Ring and vibrate logic
assign ringer = ring & ~vibrate_mode; // Enable ringer if ring is 1 and vibrate_mode is 0
assign motor = ring & vibrate_mode;   // Enable motor if ring is 1 and vibrate_mode is 1

endmodule
