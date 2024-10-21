module TopModule(
    input clk,
    input areset,
    input predict_valid,
    input predict_taken,
    input train_mispredicted,
    input train_taken,
    input [31:0] train_history,
    output reg [31:0] predict_history
);

always @(posedge clk or posedge areset) begin
    if (areset) begin
        predict_history <= 32'b0; // Asynchronous reset
    end else if (train_mispredicted) begin
        predict_history <= {train_history[30:0], train_taken}; // Load correct history on misprediction
    end else if (predict_valid) begin
        predict_history <= {predict_history[30:0], predict_taken}; // Shift in predict_taken
    end
end

endmodule
