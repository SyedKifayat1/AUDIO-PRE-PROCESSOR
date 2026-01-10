`timescale 1ns / 1ps
module input_buffer (
    input clk,
    input rst,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);
always @(posedge clk) begin
    if (rst)
        out_sample <= 0;
    else
        out_sample <= in_sample;
end
endmodule
