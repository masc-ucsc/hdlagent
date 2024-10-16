module shift_register #(parameter WIDTH = 8) (
    input clk,
    input rst,
    input enable,
    input [WIDTH-1:0] data_in,
    input scan_enable,
    input scan_in,
    output reg [WIDTH-1:0] data_out,
    output reg scan_out
);
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            data_out <= {WIDTH{1'b0}};
            scan_out <= 1'b0;
        end else if (scan_enable) begin
            {scan_out, data_out} <= {data_out[WIDTH-1:1], scan_in};
        end else if (enable) begin
            data_out <= data_in;
        end
    end
endmodule
module memory_bank_spec #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 8,
    parameter MEM_SIZE = 256,
    parameter IO_ADDR = 255
)(
    input clk,
    input rst,
    input [ADDR_WIDTH-1:0] address,
    input [DATA_WIDTH-1:0] data_in,
    input write_enable,
    output reg [DATA_WIDTH-1:0] data_out,
    input scan_enable,
    input scan_in,
    output scan_out,
    input btn_in,
    output reg [6:0] led_out
);

    reg [MEM_SIZE-1:0] memory_enable;
    wire [DATA_WIDTH-1:0] memory_out [MEM_SIZE-1:0];
    wire io_scan_out;
    wire memory_scan_chain [0:MEM_SIZE-1];

    // Generate instantiated shift_registers for memory cells
    genvar i;
    generate
        for (i = 0; i < MEM_SIZE; i = i + 1) begin : memory_cells
            shift_register #(DATA_WIDTH) memory_cell (
                .clk(clk),
                .rst(rst),
                .enable(memory_enable[i]),
                .data_in(data_in),
                .scan_enable(scan_enable),
                .scan_in(i == 0 ? scan_in : memory_scan_chain[i-1]),
                .data_out(memory_out[i]),
                .scan_out(memory_scan_chain[i])
            );
        end
    endgenerate

    // IO handling
    shift_register #(1) btn_register (
        .clk(clk),
        .rst(rst),
        .enable(1'b0),
        .data_in(1'b0),
        .scan_enable(scan_enable),
        .scan_in(memory_scan_chain[MEM_SIZE-1]),
        .data_out(),
        .scan_out(io_scan_out)
    );

    shift_register #(7) led_register (
        .clk(clk),
        .rst(rst),
        .enable(write_enable && (address == IO_ADDR)),
        .data_in(data_in[6:0]),
        .scan_enable(scan_enable),
        .scan_in(io_scan_out),
        .data_out(led_out),
        .scan_out(scan_out)
    );

    // Address decoder for write enable signals
    integer j;
    always @* begin
        for (j = 0; j < MEM_SIZE; j = j + 1) begin
            memory_enable[j] = (address == j && write_enable) ? 1'b1 : 1'b0;
        end
    end

    // Data output selection based on address
    always @(*) begin
        if (address == IO_ADDR) begin
            data_out = {1'b0, btn_in, led_out};
        end else if (address < MEM_SIZE) begin
            data_out = memory_out[address];
        end else begin
            data_out = {DATA_WIDTH{1'b0}};
        end
    end
    
endmodule
