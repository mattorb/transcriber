#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input file> <output file>"
    exit 1
fi

input="$1"
output="$2"

ffmpeg -i "$input" -af "highpass=f=200, lowpass=f=3000, atempo=1.0, volume=1.0" -ar 16000 "$output"
