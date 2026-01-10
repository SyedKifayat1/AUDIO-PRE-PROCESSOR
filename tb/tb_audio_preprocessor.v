module tb_audio_preprocessor;

reg clk = 0;
reg rst = 1;
reg signed [15:0] audio_in;
wire signed [15:0] audio_out;

integer fin, fout;

audio_preprocessor DUT (
    .clk(clk),
    .rst(rst),
    .audio_in(audio_in),
    .audio_out(audio_out)
);

always #10 clk = ~clk;

initial begin
    fin = $fopen("audio_input.txt", "r");
    fout = $fopen("../output/vivado_output.txt", "w");

    #50 rst = 0;

    while (!$feof(fin)) begin
        $fscanf(fin, "%d\n", audio_in);
        #20;
        $fwrite(fout, "%d\n", audio_out);
    end

    $fclose(fin);
    $fclose(fout);
    $stop;
end

endmodule
