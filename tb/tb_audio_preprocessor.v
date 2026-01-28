module tb_audio_preprocessor;

reg clk = 0;
reg rst = 1;
reg [1:0] filter_sel = 0;
reg signed [15:0] audio_in;
wire signed [15:0] audio_out;

integer fin, fout;
integer sample_cnt = 0;
integer mode_file;
integer mode_val;

audio_preprocessor DUT (
    .clk(clk),
    .rst(rst),
    .filter_sel(filter_sel),
    .audio_in(audio_in),
    .audio_out(audio_out)
);

always #10 clk = ~clk;

initial begin
    fin = $fopen("E:/GitHub Data/AUDIO-PRE-PROCESSOR/tb/audio_input.txt", "r");
    fout = $fopen("E:/GitHub Data/AUDIO-PRE-PROCESSOR/output/vivado_output.txt", "w");

    #50 rst = 0;

    // Read Filter Mode from external file
    mode_file = $fopen("E:/GitHub Data/AUDIO-PRE-PROCESSOR/tb/filter_mode.txt", "r");
    if (mode_file == 0) begin
        filter_sel = 0; // Default to Bass if file missing
    end else begin
        $fscanf(mode_file, "%d", mode_val);
        filter_sel = mode_val[1:0];
        $fclose(mode_file);
    end

    while (!$feof(fin)) begin
        $fscanf(fin, "%d\n", audio_in);
        
        // No dynamic switching - use the loaded mode
        sample_cnt = sample_cnt + 1;
        
        #20;
        $fwrite(fout, "%d\n", audio_out);
    end

    $fclose(fin);
    $fclose(fout);
    $stop;
end

endmodule
