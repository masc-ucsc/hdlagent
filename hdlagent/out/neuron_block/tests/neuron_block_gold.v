module neuron_block (
    input [7:0] voltage_potential_i,
    input [7:0] pos_threshold_i,
    input [7:0] neg_threshold_i,
    input [7:0] leak_value_i,
    input [7:0] weight_type1_i,
    input [7:0] weight_type2_i,
    input [7:0] weight_type3_i,
    input [7:0] weight_type4_i,
    input [7:0] weight_select_i,
    input [7:0] pos_reset_i,
    input [7:0] neg_reset_i,
    input enable_i,
    output reg [7:0] new_potential_o,
    output reg spike_o
);

    reg [7:0] selected_weight;
    reg [8:0] potential_calc;


    always @(*) begin
        case(weight_select_i)
            8'd0: selected_weight = weight_type1_i;
            8'd1: selected_weight = weight_type2_i;
            8'd2: selected_weight = weight_type3_i;
            8'd3: selected_weight = weight_type4_i;
            default: selected_weight = 8'b0;
        endcase
    end


    always @(*) begin
        if (enable_i == 1) begin

            potential_calc = {1'b0, voltage_potential_i} + selected_weight - leak_value_i;


            if (potential_calc[8]) new_potential_o = 8'b00000000;
            else if (potential_calc > 8'b11111111) new_potential_o = 8'b11111111;
            else new_potential_o = potential_calc[7:0];


            if (new_potential_o >= pos_threshold_i) begin
                new_potential_o = pos_reset_i;
                spike_o = 1;
            end else if (new_potential_o <= neg_threshold_i) begin
                new_potential_o = neg_reset_i;
                spike_o = 0;
            end else begin
                spike_o = 0;
            end
        end else begin
            new_potential_o = 8'b0;
            spike_o = 0;
        end
    end

endmodule





