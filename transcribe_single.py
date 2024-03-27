import argparse
import transcriber
import sys

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some audio files.")
    parser.add_argument('audio_file', help="The audio file")

    args = parser.parse_args()

    album_name = "single"
    audio_filename = sys.argv[1]

    output_dir = Path("out/transcribe") / album_name
    output_dir.mkdir(parents=True, exist_ok=True)

    transcriber.transcribe_single(audio_filename, output_dir)
