module four_mux (
    input  [15:0] In_i,
    input  [ 3:0] S,
    output        Out_o
);

  always_comb begin
    case (S)
      4'b0000: Out_o = In_i[0];
      4'b0001: Out_o = In_i[1];
      4'b0010: Out_o = In_i[2];
      4'b0011: Out_o = In_i[3];
      4'b0100: Out_o = In_i[4];
      4'b0101: Out_o = In_i[5];
      4'b0110: Out_o = In_i[6];
      4'b0111: Out_o = In_i[7];
      4'b1000: Out_o = In_i[8];
      4'b1001: Out_o = In_i[9];
      4'b1010: Out_o = In_i[10];
      4'b1011: Out_o = In_i[11];
      4'b1100: Out_o = In_i[12];
      4'b1101: Out_o = In_i[13];
      4'b1110: Out_o = In_i[14];
      4'b1111: Out_o = In_i[15];
      default: Out_o = In_i[15];
    endcase
  end
endmodule

