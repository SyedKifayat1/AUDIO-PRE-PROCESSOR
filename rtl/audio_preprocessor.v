module audio_preprocessor (
    input clk,
    input rst,
    input [1:0] filter_sel,
    input signed [15:0] audio_in,
    output signed [15:0] audio_out
);

wire signed [15:0] buffered;
wire signed [31:0] fir_out;
wire signed [15:0] filtered_audio;
wire signed [15:0] echoed_audio;

input_buffer u_buf (
    .clk(clk), .rst(rst),
    .in_sample(audio_in), .out_sample(buffered)
);

fir_core u_fir (
    .clk(clk), .rst(rst),
    .filter_sel(filter_sel),
    .x_in(buffered), .y_out(fir_out)
);

// Gain stage comes after FIR but before Echo
gain_control u_gain (
    .in_data(fir_out), .out_data(filtered_audio)
);

// New Echo stage
echo_module u_echo (
    .clk(clk), .rst(rst),
    .audio_in(filtered_audio), .audio_out(echoed_audio)
);

assign audio_out = echoed_audio;

endmodule
