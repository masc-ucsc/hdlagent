module control_unit_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] processor_enable,
    output [0:0] processor_halted,
    input [7:0] instruction,
    input [0:0] ZF,
    output [0:0] PC_write_enable,
    output [1:0] PC_mux_select,
    output [0:0] ACC_write_enable,
    output [1:0] ACC_mux_select,
    output [0:0] IR_load_enable,
    output [3:0] ALU_opcode,
    output [0:0] ALU_inputB_mux_select,
    output [0:0] Memory_write_enable,
    output [1:0] Memory_address_mux_select,
    input [0:0] scan_enable,
    input [0:0] scan_in,
    output [0:0] scan_out
);

    // State Definitions
    localparam RESET = 2'b00, FETCH = 2'b01, EXECUTE = 2'b10, HALT = 2'b11;
    
    // State register
    reg [1:0] current_state, next_state;
    
    // State transition logic
    always @(*) begin
        if (rst) begin
            next_state = RESET;
        end else if (processor_enable) begin
            case (current_state)
                RESET: next_state = FETCH;
                FETCH: next_state = EXECUTE;
                EXECUTE: 
                    next_state = (instruction == 8'b11111111) ? HALT : FETCH;
                HALT: next_state = HALT;
                default: next_state = RESET;
            endcase
        end else begin
            next_state = current_state;
        end
    end
    
    // State register update
    always @(posedge clk or posedge rst) begin
        if (rst)
            current_state <= RESET;
        else
            current_state <= next_state;
    end
    
    // Output logic
    assign processor_halted = (current_state == HALT);
    
    assign PC_write_enable = (current_state == FETCH || current_state == EXECUTE);
    assign PC_mux_select = (current_state == FETCH) ? 2'b01 : 2'b00;
    
    assign ACC_write_enable = (current_state == EXECUTE && instruction[7:4] == 4'b0100);
    assign ACC_mux_select = (instruction[7:4] == 4'b0100) ? 2'b01 : 2'b00;
    
    assign IR_load_enable = (current_state == FETCH);

    assign ALU_opcode = (current_state == EXECUTE) ? instruction[3:0] : 4'b0000;
    assign ALU_inputB_mux_select = (instruction[7:4] == 4'b0100) ? 1'b1 : 1'b0;
    
    assign Memory_write_enable = (current_state == EXECUTE && instruction[7:4] == 4'b0010);
    assign Memory_address_mux_select = (instruction[7:4] == 4'b0010) ? 2'b01 : 2'b00;
    
    assign scan_out = scan_in; // Simplified for scan chain
    
endmodule
