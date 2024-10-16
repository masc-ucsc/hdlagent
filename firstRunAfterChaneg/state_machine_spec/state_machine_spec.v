module state_machine_spec(input [0:0] clock, input [0:0] reset, output reg [1:0] state);

  // State parameter definitions
  parameter IDLE  = 2'b00;
  parameter START = 2'b01;
  parameter RUN   = 2'b10;
  parameter STOP  = 2'b11;

  always @(*) begin
    if (reset) begin
      state = IDLE; // Reset state
    end else begin
      case (state)
        IDLE:  state = START; // Transition from IDLE to START
        START: state = RUN;   // Transition from START to RUN
        RUN:   state = STOP;  // Transition from RUN to STOP
        STOP:  state = IDLE;  // Transition from STOP back to IDLE
        default: state = IDLE; // Default state
      endcase
    end
  end

endmodule
