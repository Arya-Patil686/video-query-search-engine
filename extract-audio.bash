#!/bin/bash

# Iterate from 1 to 20
for i in {1..20}; do
    # Define input and output file names
    input_file="Data/Videos/video${i}.mp4"
    output_file="Data/Audio/Audios_DB/video${i}.wav"

    # Check if input file exists
    if [ -f "$input_file" ]; then
        echo "Processing $input_file..."

        # Extract audio from input video and save as .wav file
        ffmpeg -i "$input_file" -vn -acodec pcm_s16le -ar 44100 -ac 2 "$output_file"

        echo "Output saved as $output_file"
    else
        echo "Input file $input_file not found."
    fi
done
