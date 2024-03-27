#!/bin/bash
set -e

if ! command -v ffmpeg &> /dev/null; then
   echo "ffmpeg not found. Please install ffmpeg and try again."
   exit
fi

if [ ! -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
   echo "Conda not found. Please install conda and try again."
   exit
fi

source "$HOME/anaconda3/etc/profile.d/conda.sh"
conda create -y --name transcriber python=3.9
conda activate transcriber
git clone git@github.com:adefossez/demucs.git
cd demucs
git checkout 8174c5d2c259dabc69acd842fc4ba5111539d507
pip install soundfile # mp3 support
pip install -e .
cd ..

git clone git@github.com:ggerganov/whisper.cpp.git
pushd whisper.cpp
trap popd EXIT
# git checkout f5f159c320d3d4be0ccb9746cde5323933ebc453
make -j
cd models
# See https://huggingface.co/ggerganov/whisper.cpp for more options
curl -L 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin?download=true' -o ggml-large-v3.bin

pip install tqdm
pip install requests

cat << EOF
Next Steps:
   $ conda activate transcriber
   $ python transcribe_single.py in/myfile.mp3
   $ # See json and txt files generated in out/whisper/
EOF