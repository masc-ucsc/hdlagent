module signal_alert (
    input clock,
    input reset,
     input sig,
    output reg high_alert,
    output reg low_alert
);
  reg [1:0] high_counter, low_counter;

  always @(posedge clock) begin
    if (reset) begin high_counter <= 'b0; low_counter <= 'b0; end else if (sig) begin
      high_counter <= high_counter + 1;
      low_counter  <= 'b0;
    end else begin
      low_counter  <= low_counter + 1;
      high_counter <= 'b0;
    end
  end assign high_alert = (high_counter == 2'b11) ? 1'b1 : 1'b0;
   assign low_alert  = (low_counter == 2'b11) ? 1'b1 : 1'b0;
endmodule

