`timescale 1ns / 1ps
module fir_core (
    input clk,
    input rst,
    input signed [15:0] x_in,
    output reg signed [31:0] y_out
);

parameter TAPS = 5;

reg signed [15:0] coeff [0:TAPS-1];
reg signed [15:0] shift [0:TAPS-1];
integer i;

initial begin
    // Corrected Signed Decimal Syntax: -Width'sdValue
    coeff[0] = 16'sd2000;   // Soft Bass
    coeff[1] = 16'sd6000;   // Lower-Mid
    coeff[2] = 16'sd10000;  // Center (Voice Clarity)
    coeff[3] = 16'sd6000;   // Lower-Mid
    coeff[4] = 16'sd2000;   // Soft Bass
end

always @(posedge clk) begin
    if (rst) begin
        for (i=0;i<TAPS;i=i+1)
            shift[i] <= 0;
        y_out <= 0;
    end else begin
        shift[0] <= x_in;
        for (i=1;i<TAPS;i=i+1)
            shift[i] <= shift[i-1];

        y_out <= shift[0]*coeff[0] +
                 shift[1]*coeff[1] +
                 shift[2]*coeff[2] +
                 shift[3]*coeff[3] +
                 shift[4]*coeff[4];
    end
end
endmodule
