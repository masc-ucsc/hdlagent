module TopModule(
    input [0:0] clk,
    input [7:0] in,
    input [0:0] reset,
    output reg [23:0] out_bytes,
    output reg [0:0] done
);

    reg [1:0] state;
    reg [23:0] message;

    parameter IDLE = 2'b00;
    parameter BYTE_1 = 2'b01;
    parameter BYTE_2 = 2'b10;
    parameter BYTE_3 = 2'b11;

    always @(posedge clk) begin
        if (reset) begin
            state <= IDLE;
            out_bytes <= 24'bx;
            done <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (in[3]) begin
                        message[23:16] <= in;
                        state <= BYTE_1;
                    end
                end
                BYTE_1: begin
                    message[15:8] <= in;
                    state <= BYTE_2;
                end
                BYTE_2: begin
                    message[7:0] <= in;
                    out_bytes <= message;
                    done <= 1;
                    state <= BYTE_3;  
                end
                BYTE_3: begin
                    done <= 0;
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
