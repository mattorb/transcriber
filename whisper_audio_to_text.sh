#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input file> <output file>"
    exit 1
fi

input="$1"
output="$2"

./whisper.cpp/main -m ./whisper.cpp/models/ggml-large-v3.bin -f "$input" -olrc -oj -otxt -of "$output" -t 16 -np