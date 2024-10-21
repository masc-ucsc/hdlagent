module TopModule(input clock, input a, output p, output q);
    reg [1:0] state; // Define a state register

    always @(posedge clock) begin
        case (state)
            2'b00: begin
                if (a) state <= 2'b01;
                else state <= 2'b00;
            end
            2'b01: begin
                if (a) state <= 2'b10;
                else state <= 2'b00;
            end
            2'b10: begin
                if (~a) state <= 2'b11;
                else state <= 2'b10;
            end
            2'b11: begin
                if (a) state <= 2'b00;
                else state <= 2'b11;
            end
            default: state <= 2'b00;
        endcase
    end

    assign p = (state == 2'b10) && a;
    assign q = (state == 2'b11);
endmodule
