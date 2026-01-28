`timescale 1ns / 1ps
module fir_core (
    input clk,
    input rst,
    input [1:0] filter_sel, // 00: Bass, 01: Treble, 10: Bandpass
    input signed [15:0] x_in,
    output reg signed [31:0] y_out
);

parameter TAPS = 5;

reg signed [15:0] coeff [0:TAPS-1];
reg signed [15:0] shift [0:TAPS-1];
integer i;

// Calculated Coefficients for Fs=48000Hz, Taps=5

always @(*) begin
    case (filter_sel)
        2'b00: begin // Bass / Low Pass (< 1kHz)
            coeff[0] = 16'sd1160;
            coeff[1] = 16'sd7894;
            coeff[2] = 16'sd14661;
            coeff[3] = 16'sd7894;
            coeff[4] = 16'sd1160;
        end
        2'b01: begin // Treble / High Pass (> 4kHz)
            coeff[0] = -16'sd368;
            coeff[1] = -16'sd2864;
            coeff[2] = 16'sd27774;
            coeff[3] = -16'sd2864;
            coeff[4] = -16'sd368;
        end
        2'b10: begin // Bandpass (Mid/High Boost > 2kHz)
            coeff[0] = -16'sd210;
            coeff[1] = -16'sd1468;
            coeff[2] = 16'sd30252;
            coeff[3] = -16'sd1468;
            coeff[4] = -16'sd210;
        end
        default: begin // Default to Bass
            coeff[0] = 16'sd1160;
            coeff[1] = 16'sd7894;
            coeff[2] = 16'sd14661;
            coeff[3] = 16'sd7894;
            coeff[4] = 16'sd1160;
        end
    endcase
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
