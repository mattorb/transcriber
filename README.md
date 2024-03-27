MP3 -> lyrics transcription pipeline using demucs, ffmpeg, and whisper.cpp

Scrappy pipeline to run locally on M2/M3 macbook.

Features
- Pipeline avoids redoing work on re-run.. caches result of each stage: stemming, trimming, asr.


1. Install anaconda
1. Install ffmpeg
1. ./init.sh

Note: has some problems with harmonies, auto-tuned, and vocals that are too far from the norm of the whisper training data.