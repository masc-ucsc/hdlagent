module mixColumns(input [127:0] state_in, output [127:0] state_out);
    function [7:0] mb2;
        input [7:0] a;
        begin
            mb2 = (a << 1) ^ (8'h1B & ((a[7] == 1'b1) ? 8'hFF : 8'h00));
        end
    endfunction

    function [7:0] mb3;
        input [7:0] a;
        begin
            mb3 = mb2(a) ^ a;
        end
    endfunction

    assign state_out[7:0] = mb2(state_in[7:0]) ^ mb3(state_in[15:8]) ^ state_in[23:16] ^ state_in[31:24];
    assign state_out[15:8] = state_in[7:0] ^ mb2(state_in[15:8]) ^ mb3(state_in[23:16]) ^ state_in[31:24];
    assign state_out[23:16] = state_in[7:0] ^ state_in[15:8] ^ mb2(state_in[23:16]) ^ mb3(state_in[31:24]);
    assign state_out[31:24] = mb3(state_in[7:0]) ^ state_in[15:8] ^ state_in[23:16] ^ mb2(state_in[31:24]);

    // and so on for the remaining state_out assignments...
endmodule