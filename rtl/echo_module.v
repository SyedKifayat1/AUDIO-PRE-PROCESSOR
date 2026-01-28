`timescale 1ns / 1ps

module echo_module (
    input clk,
    input rst,
    input signed [15:0] audio_in,
    output signed [15:0] audio_out
);

// Delay Buffer Parameters
// 48kHz sampling * 0.1s delay = 4800 samples. 
// We'll use a smaller buffer for simulation speed/resource demo: 1024 samples
parameter DELAY_SAMPLES = 1024; 
parameter GAIN_DIV = 2; // Echo is half volume (>>1)

reg signed [15:0] delay_line [0:DELAY_SAMPLES-1];
reg [$clog2(DELAY_SAMPLES)-1:0] wr_ptr;
reg [$clog2(DELAY_SAMPLES)-1:0] rd_ptr;

reg signed [15:0] delayed_sample;
wire signed [15:0] echo_mixed;

integer i;

always @(posedge clk) begin
    if (rst) begin
        // Reset pointers
        wr_ptr <= 0;
        rd_ptr <= 1; 
        delayed_sample <= 0;
    end else begin
        // Read the old sample
        delayed_sample <= delay_line[rd_ptr];
        
        // Overwrite with new sample
        delay_line[wr_ptr] <= audio_in;
        
        // Increment pointers
        wr_ptr <= wr_ptr + 1;
        rd_ptr <= rd_ptr + 1;
    end
end

// Initialize memory for simulation to avoid 'X' propagation
initial begin
    for (i = 0; i < DELAY_SAMPLES; i = i + 1) begin
        delay_line[i] = 0;
    end
end

// Mix: Original + (Delayed / 2)
// Use blocking assignment or intermediate wire for saturation logic
assign echo_mixed = audio_in + (delayed_sample >>> 1); // Simple mix

// Basic Saturation Logic
assign audio_out = echo_mixed; // For now simple assign, could add clamping if needed

endmodule
