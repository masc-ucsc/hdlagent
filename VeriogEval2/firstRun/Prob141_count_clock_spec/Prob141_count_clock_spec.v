module TopModule(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss
);

    reg [3:0] ones_sec, tens_sec;
    reg [3:0] ones_min, tens_min;
    reg [3:0] ones_hour, tens_hour;

    always @(posedge clk) begin
        if (reset) begin
            // Reset clock to 12:00:00 AM
            ones_sec <= 4'd0;
            tens_sec <= 4'd0;
            ones_min <= 4'd0;
            tens_min <= 4'd0;
            ones_hour <= 4'd2;
            tens_hour <= 4'd1;
            pm <= 1'b0;
        end else if (ena) begin
            // Increment seconds
            if (ones_sec == 4'd9) begin
                ones_sec <= 4'd0;
                if (tens_sec == 4'd5) begin
                    tens_sec <= 4'd0;
                    
                    // Increment minutes
                    if (ones_min == 4'd9) begin
                        ones_min <= 4'd0;
                        if (tens_min == 4'd5) begin
                            tens_min <= 4'd0;
                            
                            // Increment hours
                            if (ones_hour == 4'd9 || ones_hour == 4'd2) begin
                                ones_hour <= 4'd1;
                                if (tens_hour == 4'd1) begin
                                    tens_hour <= 4'd0;
                                    pm <= ~pm; // Toggle AM/PM
                                end else if (tens_hour == 4'd0) begin
                                    tens_hour <= 4'd1;
                                end
                            end else begin
                                ones_hour <= ones_hour + 4'd1;
                            end
                        end else begin
                            tens_min <= tens_min + 4'd1;
                        end
                    end else begin
                        ones_min <= ones_min + 4'd1;
                    end
                end else begin
                    tens_sec <= tens_sec + 4'd1;
                end
            end else begin
                ones_sec <= ones_sec + 4'd1;
            end
        end

        // Assigning BCD to output
        ss <= {tens_sec, ones_sec};
        mm <= {tens_min, ones_min};
        hh <= {tens_hour, ones_hour};
    end

endmodule
