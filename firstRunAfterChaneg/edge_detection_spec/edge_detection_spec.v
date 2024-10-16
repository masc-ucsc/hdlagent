module edge_detection_spec(input [0:0] inp, output [0:0] out1, output [0:0] out2);

    reg [0:0] inp_prev;

    initial begin
        inp_prev = 0; // Initialize previous input value
    end

    always @(*) begin
        if (inp == 1 && inp_prev == 0)
            out1 = 1; // Rising edge detected
        else
            out1 = 0;
    end

    always @(*) begin
        if (inp == 0 && inp_prev == 1)
            out2 = 1; // Falling edge detected
        else
            out2 = 0;
    end

    always @(*) begin
        inp_prev = inp; // Update the previous value
    end

endmodule
