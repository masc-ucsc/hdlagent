module memory_bank #(
    parameter ADDR_WIDTH = 5,
    parameter DATA_WIDTH = 8,
    parameter MEM_SIZE = 31,    parameter IO_ADDR = MEM_SIZE
)(
    input wire clk,
    input wire rst,
    input wire [ADDR_WIDTH-1:0] address,
    input wire [DATA_WIDTH-1:0] data_in,
    input wire write_enable,
    output reg [DATA_WIDTH-1:0] data_out,
    input wire scan_enable,
    input wire scan_in,
    output wire scan_out,
    input wire btn_in,   output wire [6:0] led_out );

     wire [DATA_WIDTH-1:0] mem_data_out [0:MEM_SIZE-1];
    wire mem_scan_out [0:MEM_SIZE-1];

    genvar i;
    generate
        for (i = 0; i < MEM_SIZE; i = i + 1) begin : memory
            shift_register #(
                .WIDTH(DATA_WIDTH)
            ) mem_cell (
                .clk(clk),
                .rst(rst),
                .enable(write_enable && (address == i)),
                .data_in(data_in),
                .data_out(mem_data_out[i]),
                .scan_enable(scan_enable),
                .scan_in(i == 0 ? scan_in : mem_scan_out[i-1]),
                .scan_out(mem_scan_out[i])
            );
        end
    endgenerate

     wire [6:0] led_data_out;
    wire btn_data_out;
    wire io_scan_out;
    shift_register #(
        .WIDTH(1)
    ) btn_shift_register (
        .clk(clk),
        .rst(rst),
        .enable(1'b1),        .data_in(btn_in),
        .data_out(btn_data_out),
        .scan_enable(scan_enable),
        .scan_in(mem_scan_out[MEM_SIZE-1]),        .scan_out(io_scan_out)   );

    shift_register #(
        .WIDTH(7)
    ) led_shift_register (
        .clk(clk),
        .rst(rst),
        .enable(write_enable && (address == IO_ADDR)),
        .data_in(data_in[7:1]),        .data_out(led_data_out),
        .scan_enable(scan_enable),
        .scan_in(io_scan_out),  .scan_out(scan_out)   );

  always @(*) begin
    if (address < MEM_SIZE) begin
        data_out = mem_data_out[address];
    end else case (address)
        IO_ADDR: data_out = {led_data_out, btn_data_out};   IO_ADDR + 1: data_out = IO_ADDR + 2;  IO_ADDR + 2: data_out = {7'b0111111, 1'b0};   IO_ADDR + 3: data_out = {7'b0000110, 1'b0};     IO_ADDR + 4: data_out = {7'b1011011, 1'b0};  IO_ADDR + 5: data_out = {7'b1001111, 1'b0}; IO_ADDR + 6: data_out = {7'b1100110, 1'b0};  IO_ADDR + 7: data_out = {7'b1101101, 1'b0};   IO_ADDR + 8: data_out = {7'b1111100, 1'b0};  IO_ADDR + 9: data_out = {7'b0000111, 1'b0};   IO_ADDR + 10: data_out = {7'b1111111, 1'b0};  IO_ADDR + 11: data_out = {7'b1100111, 1'b0};   default: data_out = 8'b00000001;    endcase
   end

     assign led_out = led_data_out;

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
        end else if (scan_enable) begin
            if (WIDTH == 1) begin
                internal_data <= scan_in;
            end else begin
                internal_data <= {internal_data[WIDTH-2:0], scan_in};
            end
        end else if (enable) begin
            internal_data <= data_in;
        end
    end

   assign data_out = internal_data;
    assign scan_out = internal_data[WIDTH-1];

endmodule

