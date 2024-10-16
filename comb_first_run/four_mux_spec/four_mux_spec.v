module four_mux_spec(input [15:0] In_i, input [3:0] S, output [0:0] Out_o);

  assign Out_o = (S == 4'd0)  ? In_i[0] :
                 (S == 4'd1)  ? In_i[1] :
                 (S == 4'd2)  ? In_i[2] :
                 (S == 4'd3)  ? In_i[3] :
                 (S == 4'd4)  ? In_i[4] :
                 (S == 4'd5)  ? In_i[5] :
                 (S == 4'd6)  ? In_i[6] :
                 (S == 4'd7)  ? In_i[7] :
                 (S == 4'd8)  ? In_i[8] :
                 (S == 4'd9)  ? In_i[9] :
                 (S == 4'd10) ? In_i[10] :
                 (S == 4'd11) ? In_i[11] :
                 (S == 4'd12) ? In_i[12] :
                 (S == 4'd13) ? In_i[13] :
                 (S == 4'd14) ? In_i[14] :
                                In_i[15];

endmodule
