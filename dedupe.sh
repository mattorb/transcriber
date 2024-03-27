#!/bin/bash

# whisper.cpp quirk, hallucinates previous lines transcription during silence.  see issues...timestamps 

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input file> <output file>"
    exit 1
fi

input="$1"
output="$2"

# Deduplicate sequential duplicate lines
awk '!seen[$0]++' "$input" > "$output"
