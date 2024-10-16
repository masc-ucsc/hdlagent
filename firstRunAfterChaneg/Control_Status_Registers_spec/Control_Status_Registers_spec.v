module Control_Status_Registers_spec(
    input [0:0] clk,
    input [0:0] rst,
    input [2:0] addr,
    input [WIDTH-1:0] data_in,
    input [0:0] wr_enable,
    input [WIDTH-1:0] IO_IN,
    input [0:0] processor_enable,
    input [0:0] scan_enable,
    input [0:0] scan_in,
    output [WIDTH-1:0] data_out,
    output [WIDTH-1:0] SEGEXE_L_OUT,
    output [WIDTH-1:0] SEGEXE_H_OUT,
    output [WIDTH-1:0] IO_OUT,
    output [0:0] INT_OUT,
    output [0:0] scan_out
);

wire [WIDTH-1:0] segexe_l_data;
wire [WIDTH-1:0] segexe_h_data;
wire [WIDTH-1:0] io_in_data;
wire [WIDTH-1:0] io_out_data;
wire [WIDTH-1:0] cnt_l_data;
wire [WIDTH-1:0] cnt_h_data;
wire [WIDTH-1:0] status_ctrl_data;
wire [WIDTH-1:0] temp_data;

wire segexe_l_scan_out;
wire segexe_h_scan_out;
wire io_in_scan_out;
wire io_out_scan_out;
wire cnt_l_scan_out;
wire cnt_h_scan_out;
wire status_ctrl_scan_out;
wire temp_scan_out;

// Shift register instantiations
shift_register #(.WIDTH(WIDTH)) segexe_l_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd0)), // Load if address matches
    .data_in(data_in),
    .data_out(segexe_l_data),
    .scan_enable(scan_enable),
    .scan_in(scan_in),
    .scan_out(segexe_l_scan_out)
);

shift_register #(.WIDTH(WIDTH)) segexe_h_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd1)),
    .data_in(data_in),
    .data_out(segexe_h_data),
    .scan_enable(scan_enable),
    .scan_in(segexe_l_scan_out),
    .scan_out(segexe_h_scan_out)
);

shift_register #(.WIDTH(WIDTH)) io_in_reg (
    .clk(clk),
    .rst(rst),
    .enable(processor_enable), // Always enabled
    .data_in(IO_IN),
    .data_out(io_in_data),
    .scan_enable(scan_enable),
    .scan_in(segexe_h_scan_out),
    .scan_out(io_in_scan_out)
);

shift_register #(.WIDTH(WIDTH)) io_out_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd2)),
    .data_in(data_in),
    .data_out(io_out_data),
    .scan_enable(scan_enable),
    .scan_in(io_in_scan_out),
    .scan_out(io_out_scan_out)
);

shift_register #(.WIDTH(WIDTH)) cnt_l_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd3)),
    .data_in(data_in),
    .data_out(cnt_l_data),
    .scan_enable(scan_enable),
    .scan_in(io_out_scan_out),
    .scan_out(cnt_l_scan_out)
);

shift_register #(.WIDTH(WIDTH)) cnt_h_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd4)),
    .data_in(data_in),
    .data_out(cnt_h_data),
    .scan_enable(scan_enable),
    .scan_in(cnt_l_scan_out),
    .scan_out(cnt_h_scan_out)
);

shift_register #(.WIDTH(WIDTH)) status_ctrl_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd5)),
    .data_in(data_in),
    .data_out(status_ctrl_data),
    .scan_enable(scan_enable),
    .scan_in(cnt_h_scan_out),
    .scan_out(status_ctrl_scan_out)
);

shift_register #(.WIDTH(WIDTH)) temp_reg (
    .clk(clk),
    .rst(rst),
    .enable(wr_enable & (addr == 3'd6)),
    .data_in(data_in),
    .data_out(temp_data),
    .scan_enable(scan_enable),
    .scan_in(status_ctrl_scan_out),
    .scan_out(temp_scan_out)
);

// Assign outputs
assign data_out = (addr == 3'd0) ? segexe_l_data :
                  (addr == 3'd1) ? segexe_h_data :
                  (addr == 3'd2) ? io_out_data :
                  (addr == 3'd3) ? cnt_l_data :
                  (addr == 3'd4) ? cnt_h_data :
                  (addr == 3'd5) ? status_ctrl_data :
                  (addr == 3'd6) ? temp_data :
                                  {WIDTH{1'b0}};

assign SEGEXE_L_OUT = segexe_l_data;
assign SEGEXE_H_OUT = segexe_h_data;
assign IO_OUT = io_out_data;
assign INT_OUT = status_ctrl_data[0]; // Connected to the bottom bit of status_ctrl_data
assign scan_out = temp_scan_out;

endmodule
