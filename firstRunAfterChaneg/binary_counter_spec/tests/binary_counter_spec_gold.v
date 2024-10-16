module counter (
    input wire CE,
    input wire UpDown,
    input wire reset,
    input wire clock,
    output reg [7:0] CountOut
);


  always @(posedge clock) begin

    if (reset) begin

      CountOut <= 8'd0;
    end
    else if (CE) begin

      if (UpDown) begin

        CountOut <= CountOut + 1;
      end else begin

        CountOut <= CountOut - 1;
      end
    end
  end
endmodule

