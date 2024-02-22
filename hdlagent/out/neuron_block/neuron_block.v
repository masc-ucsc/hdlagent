module neuron_block(
    input  [7:0] voltage_potential_i,
    input  [7:0] pos_threshold_i,
    input  [7:0] neg_threshold_i,
    input  [7:0] leak_value_i,
    input  [7:0] weight_type1_i,
    input  [7:0] weight_type2_i,
    input  [7:0] weight_type3_i,
    input  [7:0] weight_type4_i,
    input  [7:0] weight_select_i,
    input  [7:0] pos_reset_i,
    input  [7:0] neg_reset_i,
    input  [0:0] enable_i,
    output reg [7:0] new_potential_o,
    output reg spike_o
);
    wire [7:0] weight;
    wire [7:0] new_potential;
    wire pos_spike;
    wire neg_spike;
    
    // Logic to select the weight based on weight_select_i
    assign weight = (weight_select_i == 1) ? weight_type1_i : (weight_select_i == 2) ? weight_type2_i : (weight_select_i == 3) ? weight_type3_i : weight_type4_i;

    // Logic to calculate the new potential using the selected weight.
    assign new_potential = voltage_potential_i + weight - leak_value_i;

    // Overflow and underflow protection
    assign new_potential_o = (new_potential > 255) ? 255 : (new_potential < 0) ? 0 : new_potential;

    // Check for positive threshold crossing
    assign pos_spike = (new_potential_o >= pos_threshold_i);

    // Check for negative threshold crossing
    assign neg_spike = (new_potential_o <= neg_threshold_i);

    // Update spike_o based on threshold crossings
    assign spike_o = pos_spike | neg_spike;
   
    // Reset behaviour for enable signal  
    always @(enable_i)
    begin
        if(enable_i == 1)
        begin
            spike_o <= pos_spike | neg_spike;
            new_potential_o <= (pos_spike) ? pos_reset_i : (neg_spike) ? neg_reset_i : new_potential_o;
        end
        else
        begin
            spike_o <= 0;
            new_potential_o <= 0;
        end
    end
endmodule