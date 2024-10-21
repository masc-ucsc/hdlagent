module TopModule(input [7:0] code, output [3:0] out, output [0:0] valid);

  reg [3:0] out_reg;
  reg valid_reg;

  always @(*) begin
    case (code)
      8'h45: begin
        out_reg = 4'd0;
        valid_reg = 1'b1;
      end
      8'h16: begin
        out_reg = 4'd1;
        valid_reg = 1'b1;
      end
      8'h1E: begin
        out_reg = 4'd2;
        valid_reg = 1'b1;
      end
      8'h26: begin
        out_reg = 4'd3;
        valid_reg = 1'b1;
      end
      8'h25: begin
        out_reg = 4'd4;
        valid_reg = 1'b1;
      end
      8'h2E: begin
        out_reg = 4'd5;
        valid_reg = 1'b1;
      end
      8'h36: begin
        out_reg = 4'd6;
        valid_reg = 1'b1;
      end
      8'h3D: begin
        out_reg = 4'd7;
        valid_reg = 1'b1;
      end
      8'h3E: begin
        out_reg = 4'd8;
        valid_reg = 1'b1;
      end
      8'h46: begin
        out_reg = 4'd9;
        valid_reg = 1'b1;
      end
      default: begin
        out_reg = 4'd0;
        valid_reg = 1'b0;
      end
    endcase
  end

  assign out = out_reg;
  assign valid = valid_reg;

endmodule
