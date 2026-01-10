module gain_control (
    input signed [31:0] in_data,
    output signed [15:0] out_data
);
assign out_data = in_data >>> 15; // Normalize back to 16-bit
endmodule
