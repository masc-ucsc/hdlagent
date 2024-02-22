module async_dualram_16X8(
    input cs,
    input rst,
    input wr_enb,
    input [3:0] wr_addr,
    input [7:0] wr_data,
    input rd_enb,
    input [3:0] rd_addr,
    output reg [7:0] rd_data
    );

    // Define parameters for addressing and data width
    parameter ADDR_WIDTH=4, DEPTH=16, DATA_WIDTH=8;

    // Declare the RAM memory array
    reg [DATA_WIDTH-1:0] ram [0:DEPTH-1];

    // Memory reset
    integer i;
    initial begin
        for (i = 0; i < DEPTH; i = i + 1)
            ram[i] = 8'b0;
    end

    // Write operation
    always @(rst or cs or wr_enb or wr_addr or wr_data) begin
        integer addr = wr_addr;       // Cast array intance size
        if (rst) 
            ram[addr] = 8'b0;         // Reset the addressed data
        else if (cs && wr_enb) 
            ram[addr] = wr_data;      // Write new data to addressed loaction
    end

    // Read operation
    always @(rst or cs or rd_enb or rd_addr) begin
        integer addr = rd_addr;       // Cast array intance size
        if (rst) 
            rd_data = 8'b0;           // Reset the read data
        else if (cs && rd_enb) 
            rd_data = ram[addr];      // Read data from addressed location
    end
endmodule