module TopModule (input a, input b, input c, input d, input e, output [24:0] out);
    assign out[24] = ~(a ^ a); // a compared with a
    assign out[23] = ~(a ^ b); // a compared with b
    assign out[22] = ~(a ^ c); // a compared with c
    assign out[21] = ~(a ^ d); // a compared with d
    assign out[20] = ~(a ^ e); // a compared with e
    assign out[19] = ~(b ^ a); // b compared with a
    assign out[18] = ~(b ^ b); // b compared with b
    assign out[17] = ~(b ^ c); // b compared with c
    assign out[16] = ~(b ^ d); // b compared with d
    assign out[15] = ~(b ^ e); // b compared with e
    assign out[14] = ~(c ^ a); // c compared with a
    assign out[13] = ~(c ^ b); // c compared with b
    assign out[12] = ~(c ^ c); // c compared with c
    assign out[11] = ~(c ^ d); // c compared with d
    assign out[10] = ~(c ^ e); // c compared with e
    assign out[9]  = ~(d ^ a); // d compared with a
    assign out[8]  = ~(d ^ b); // d compared with b
    assign out[7]  = ~(d ^ c); // d compared with c
    assign out[6]  = ~(d ^ d); // d compared with d
    assign out[5]  = ~(d ^ e); // d compared with e
    assign out[4]  = ~(e ^ a); // e compared with a
    assign out[3]  = ~(e ^ b); // e compared with b
    assign out[2]  = ~(e ^ c); // e compared with c
    assign out[1]  = ~(e ^ d); // e compared with d
    assign out[0]  = ~(e ^ e); // e compared with e
endmodule
