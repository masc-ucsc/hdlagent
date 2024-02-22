module inverseMixColumns
(
  input  [127:0] state_in,
  output [127:0] state_out
);

  // Function for multiplication in AES in GF(2^8)
  function [7:0] multiply;
    input [7:0] x;
    input [7:0] y;
    integer i;
    reg [7:0] z;
    begin
      z = 8'b00000000;
      for (i = 0; i < 8; i = i + 1) begin
        if (y[i]==1'b1) z = z ^ x;
        x = (x[7]==1'b1) ? ((x<<1)^8'h1b) : (x<<1);
      end
      multiply = z;
    end
  endfunction
  
  // Calculate inverse mix columns for each 32-bit word (column) of the state
  assign state_out[31:0] = {multiply(8'he, state_in[7:0]), multiply(8'hb, state_in[15:8]), multiply(8'hd, state_in[23:16]), multiply(8'h9, state_in[31:24])};
  assign state_out[63:32] = {multiply(8'he, state_in[39:32]), multiply(8'hb, state_in[47:40]), multiply(8'hd, state_in[55:48]), multiply(8'h9, state_in[63:56])};
  assign state_out[95:64] = {multiply(8'he, state_in[71:64]), multiply(8'hb, state_in[79:72]), multiply(8'hd, state_in[87:80]), multiply(8'h9, state_in[95:88])};
  assign state_out[127:96] = {multiply(8'he, state_in[103:96]), multiply(8'hb, state_in[111:104]), multiply(8'hd, state_in[119:112]), multiply(8'h9, state_in[127:120])};

endmodule