#!/bin/bash

mkdir -p "./Data/downsampled_videos"
# Iterate from 1 to 20
for i in {11..20}; do
    # Define input and output file names
    input_file="./Data/Videos/video${i}.mp4"
    output_file="./Data/downsampled_videos/video${i}.mp4"

    # Check if input file exists
    if [ -f "$input_file" ]; then
        echo "Processing $input_file..."

        # Extract audio from input video and save as .wav file
        # ffmpeg -i "$input_file" -vn -acodec pcm_s16le -ar 10000 -ac 1 "$output_file"
        ffmpeg -y -i "$input_file"  -vf "scale=176:144" -r 30 -c:v libx264 -profile:v high -pix_fmt yuv420p -level 1.1 -color_primaries bt470bg -color_trc bt709 -colorspace smpte170m -b:v 163k -bits_per_raw_sample 8 -preset slower -c:a copy "$output_file"

        echo "Output saved as $output_file"
    else
        echo "Input file $input_file not found."
    fi
done
