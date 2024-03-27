#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input file> <output file>"
    exit 1
fi

input="$1"
output="$2"

# uses FFmpeg's silencedetect filter to analyze the audio file and find points where silence begins (silence_start) and ends (silence_end).
# It specifically looks for the _last_ occurrence of silence_start in the output. This is assumed to be the start of a silent section towards the end of the audio file.
# The script then uses the atrim filter to trim the audio file, cutting off the portion from this last silence_start point to the end of the file.

# Detect the silence and get the time when it starts
# -30dB:d=0.5 is the threshold for silence detection. Adjust as needed.
silence_start=$(ffmpeg -i "$input" -af silencedetect=noise=-11dB:d=2.0 -f null - 2>&1 | grep 'silence_start:' | tail -1 | awk '{ print $5 }')

# Check if silence is detected and trim the audio
if [ -n "$silence_start" ]; then
    ffmpeg -i "$input" -af atrim=end="$silence_start" "$output"
else
    echo "No silence detected, or the silence is at the beginning of the file."
fi