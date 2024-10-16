module control_unit (
  input wire clk,
  input wire rst,
  input wire processor_enable,
  output wire processor_halted,
  input wire [7:0] instruction,
  input wire ZF,
  output wire PC_write_enable,
  output wire [1:0] PC_mux_select,
  output wire ACC_write_enable,
  output wire [1:0] ACC_mux_select,
  output wire IR_load_enable,
  output wire [3:0] ALU_opcode,
  output wire ALU_inputB_mux_select,
  output wire Memory_write_enable,
  output wire [1:0] Memory_address_mux_select,
  input wire scan_enable,
  input wire scan_in,
  output wire scan_out
);

  localparam STATE_RESET = 3'b000;
  localparam STATE_FETCH = 3'b001;
  localparam STATE_EXECUTE = 3'b010;
  localparam STATE_HALT = 3'b100;

   reg [2:0] state_in;
  wire [2:0] state_out;
  shift_register #(
    .WIDTH(3)
  ) state_register (
    .clk(clk),
    .rst(rst),
    .enable(processor_enable),
    .data_in(state_in),
    .data_out(state_out),
    .scan_enable(scan_enable),
    .scan_in(scan_in),
    .scan_out(scan_out)
  );


always @(*) begin

  state_in = state_out;


  processor_halted = 0;

   if (processor_enable) begin
    case (state_out)
      STATE_RESET: begin
              if (!rst) begin
          state_in = STATE_FETCH;
        end
      end

      STATE_FETCH: begin
          if (instruction == 8'b11111111) begin
          state_in = STATE_HALT;
        end

        else begin
          state_in = STATE_EXECUTE;
        end
      end

      STATE_EXECUTE: begin

        if (instruction == 8'b11111111) begin
          state_in = STATE_HALT;
        end
              else begin
          state_in = STATE_FETCH;
        end
      end

      STATE_HALT: begin
             if (rst) begin
          state_in = STATE_FETCH;
        end

        else begin
          processor_halted = 1;
        end
      end

      default: begin
             state_in = STATE_FETCH;
        processor_halted = 0;
      end
    endcase
  end
end
endmodule

module shift_register #(
    parameter WIDTH = 8
)(
    input wire clk,
    input wire rst,
    input wire enable,
    input wire [WIDTH-1:0] data_in,
    output wire [WIDTH-1:0] data_out,
    input wire scan_enable,
    input wire scan_in,
    output wire scan_out
);

    reg [WIDTH-1:0] internal_data;

       always @(posedge clk) begin
        if (rst) begin
            internal_data <= {WIDTH{1'b0}};
        end else if (enable) begin
            internal_data <= data_in;
        end else if (scan_enable) begin
            internal_data <= {internal_data[WIDTH-2:0], scan_in};
        end
    end

        assign data_out = internal_data;
    assign scan_out = internal_data[WIDTH-1];

endmodule

