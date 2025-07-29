#!/bin/bash

mkdir -p "queries/10k"
# Iterate from 1 to 20
for i in {1..10}; do
    # Define input and output file names
    input_file="queries/Audio Files/video${i}_1_modified.wav"
    output_file="queries/10k/video${i}_1_10k.wav"

    # Check if input file exists
    if [ -f "$input_file" ]; then
        echo "Processing $input_file..."

        # Extract audio from input video and save as .wav file
        ffmpeg -i "$input_file" -vn -acodec pcm_s16le -ar 10000 -ac 1 "$output_file"

        echo "Output saved as $output_file"
    else
        echo "Input file $input_file not found."
    fi
done
