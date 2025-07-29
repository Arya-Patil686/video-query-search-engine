#!/bin/bash

# Iterate from 1 to 20
for i in {1..10}; do
    # Define input and output file names
    # input_file="Data/Videos/video${i}.mp4"
    video_file="Data/Queries/video${i}_1.mp4"
		audio_file="queries/Audio Files/video${i}_1.wav"

    # Check if input file exists
    if [ -f "$video_file" ]; then
        echo "Processing $video_file..."

        # Extract audio from input video and save as .wav file
        # ffmpeg -i "$input_file" -vn -acodec pcm_s16le -ar 44100 -ac 2 "$output_file"
				python Code/main.py "$video_file" "$audio_file"

        # echo "Output saved as $output_file"
    else
        echo "Input file $input_file not found."
    fi
done
