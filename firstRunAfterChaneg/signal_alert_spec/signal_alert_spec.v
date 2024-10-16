module signal_alert_spec(
    input [0:0] clock,
    input [0:0] reset,
    input [0:0] sig,
    output reg [0:0] high_alert,
    output reg [0:0] low_alert
);

    reg [1:0] high_counter; // counter for consecutive highs
    reg [1:0] low_counter;  // counter for consecutive lows

    always @(posedge clock) begin
        if (reset) begin
            high_counter <= 2'b00;
            low_counter <= 2'b00;
            high_alert <= 1'b0;
            low_alert <= 1'b0;
        end else begin
            // Monitor 'sig' for high alert
            if (sig) begin
                high_counter <= high_counter + 1;
                low_counter <= 2'b00; // reset low counter
            end else begin
                high_counter <= 2'b00; // reset high counter
                low_counter <= low_counter + 1;
            end
            
            // Set high_alert if high_counter is 3 (binary 11)
            if (high_counter == 2'b10) begin
                high_alert <= 1'b1;
            end else begin
                high_alert <= 1'b0;
            end
            
            // Set low_alert if low_counter is 3 (binary 11)
            if (low_counter == 2'b10) begin
                low_alert <= 1'b1;
            end else begin
                low_alert <= 1'b0;
            end
        end
    end
endmodule
