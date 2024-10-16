module state_machine (
    input clock,
    input reset,
    output reg [1:0] state
);

  parameter reg [1:0] IDLE = 2'b00, START = 2'b01, RUN = 2'b10, STOP = 2'b11;

  always @(posedge clock or posedge reset) begin
    if (reset) state <= IDLE;
    else
      case (state)
        IDLE: state <= START;
        START: state <= RUN;
        RUN: state <= STOP;
        STOP: state <= IDLE;
        default: state <= IDLE;
      endcase
  end

endmodule

