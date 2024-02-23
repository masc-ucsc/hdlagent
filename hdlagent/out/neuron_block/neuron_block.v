module neuron_block(
  input [7:0] voltage_potential_i, pos_threshold_i, neg_threshold_i, leak_value_i, 
  weight_type1_i, weight_type2_i, weight_type3_i, weight_type4_i, 
  weight_select_i, pos_reset_i, neg_reset_i, 
  input enable_i,
  output reg [7:0] new_potential_o,
  output reg spike_o
);

  wire [7:0] selected_weight;
  reg [7:0] temp_potential;

  // Select weight based on weight_select_i
  always @* begin
    case (weight_select_i)
      8'd0: selected_weight = weight_type1_i;
      8'd1: selected_weight = weight_type2_i;
      8'd2: selected_weight = weight_type3_i;
      8'd3: selected_weight = weight_type4_i;
      default: selected_weight = 8'd0;
    endcase	
  end

  // Calculate the updated potential using selected weight, taking care of overflow and underflow
  always @* begin
    temp_potential = voltage_potential_i + selected_weight;
    if(temp_potential < voltage_potential_i)
      temp_potential = 8'd255; // overflow case
	  
    temp_potential = temp_potential - leak_value_i;
    if(temp_potential > voltage_potential_i)
      temp_potential = 8'd0; // underflow case
  end

  // Determine spiking behavior based on the threshold values and potential resets.
  always @* begin
    if(temp_potential >= pos_threshold_i)
      begin
        spike_o = 1;
        new_potential_o = pos_reset_i;
      end
    else if(temp_potential <= neg_threshold_i)
      begin
        spike_o = 0;
        new_potential_o = neg_reset_i;
      end
    else
      begin
        spike_o = 0;
        new_potential_o = temp_potential;
      end   
  end

  // If not enabled, reset outputs
  always @(negedge enable_i) begin
    new_potential_o = 8'd0;
    spike_o = 1'b0;
  end  
  
endmodule