module variable_logical_leftshift_spec(
    input [4:0] shift_n_i,
    input [31:0] val_i,
    output [31:0] result_o
);

assign result_o = (shift_n_i == 5'd0) ? val_i :
                  (shift_n_i == 5'd1) ? {val_i[30:0], 1'b0} :
                  (shift_n_i == 5'd2) ? {val_i[29:0], 2'b0} :
                  (shift_n_i == 5'd3) ? {val_i[28:0], 3'b0} :
                  (shift_n_i == 5'd4) ? {val_i[27:0], 4'b0} :
                  (shift_n_i == 5'd5) ? {val_i[26:0], 5'b0} :
                  (shift_n_i == 5'd6) ? {val_i[25:0], 6'b0} :
                  (shift_n_i == 5'd7) ? {val_i[24:0], 7'b0} :
                  (shift_n_i == 5'd8) ? {val_i[23:0], 8'b0} :
                  (shift_n_i == 5'd9) ? {val_i[22:0], 9'b0} :
                  (shift_n_i == 5'd10) ? {val_i[21:0], 10'b0} :
                  (shift_n_i == 5'd11) ? {val_i[20:0], 11'b0} :
                  (shift_n_i == 5'd12) ? {val_i[19:0], 12'b0} :
                  (shift_n_i == 5'd13) ? {val_i[18:0], 13'b0} :
                  (shift_n_i == 5'd14) ? {val_i[17:0], 14'b0} :
                  (shift_n_i == 5'd15) ? {val_i[16:0], 15'b0} :
                  (shift_n_i == 5'd16) ? {val_i[15:0], 16'b0} :
                  (shift_n_i == 5'd17) ? {val_i[14:0], 17'b0} :
                  (shift_n_i == 5'd18) ? {val_i[13:0], 18'b0} :
                  (shift_n_i == 5'd19) ? {val_i[12:0], 19'b0} :
                  (shift_n_i == 5'd20) ? {val_i[11:0], 20'b0} :
                  (shift_n_i == 5'd21) ? {val_i[10:0], 21'b0} :
                  (shift_n_i == 5'd22) ? {val_i[9:0], 22'b0} :
                  (shift_n_i == 5'd23) ? {val_i[8:0], 23'b0} :
                  (shift_n_i == 5'd24) ? {val_i[7:0], 24'b0} :
                  (shift_n_i == 5'd25) ? {val_i[6:0], 25'b0} :
                  (shift_n_i == 5'd26) ? {val_i[5:0], 26'b0} :
                  (shift_n_i == 5'd27) ? {val_i[4:0], 27'b0} :
                  (shift_n_i == 5'd28) ? {val_i[3:0], 28'b0} :
                  (shift_n_i == 5'd29) ? {val_i[2:0], 29'b0} :
                  (shift_n_i == 5'd30) ? {val_i[1:0], 30'b0} :
                                         {val_i[0], 31'b0};

endmodule
