import subprocess
import os
from pathlib import Path


def demucs(audio_file_path, output_dir):
    print(f"Processing {audio_file_path} into {output_dir}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    subprocess.run(['demucs', '-n', 'htdemucs', '-o', output_dir, '-d', 'mps', audio_file_path])

def trim_trailing_silence(audio_file_path, output_path):
    print(f"Trimming silence from {audio_file_path} to {output_path}")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    args = ['./trim_trailing_silence.sh', audio_file_path, output_path]
    subprocess.run(args)

def attune_for_whisper(audio_file_path, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    print(f"attune (for whisper) audio from {audio_file_path} to {output_path}")
    subprocess.run(['./attune_for_whisper.sh', audio_file_path, output_path])

def whisper_audio_to_text(audio_file_path, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    print(f"Transcribing whisper audio from {audio_file_path} to {output_path}")
    subprocess.run(['./whisper_audio_to_text.sh', audio_file_path, output_path])

def dedupe_text_transcription(input_path, output_path):
    print(f"Deduping text transcription from {input_path} to {output_path}")
    subprocess.run(['./dedupe.sh', input_path, output_path])

def transcribe_single(audio_file_path, output_dir):
    basename = Path(audio_file_path).stem # track name
    vocals_path = f"{output_dir}/demucs/htdemucs/{basename}/vocals.wav"
    trimmed_path = f"{output_dir}/ffmpeg/{basename}/vocals_trimmed.wav"
    attuned_path = f"{output_dir}/ffmpeg/{basename}/vocals_attuned.wav"
    attunedtrim_path = f"{output_dir}/ffmpeg/{basename}/vocals_attunedtrim.wav"
    text_output_path = f"{output_dir}/whisper/{basename}"
    text_transcription_path = f"{output_dir}/whisper/{basename}.txt"
    text_transcription_dedupe_path = f"{output_dir}/whisper/{basename}_dedupe.txt"

    # Don't need these...wipe them
    bass_path = f"{output_dir}/demucs/htdemucs/{basename}/bass.wav"
    drums_path = f"{output_dir}/demucs/htdemucs/{basename}/drums.wav"
    other_path = f"{output_dir}/demucs/htdemucs/{basename}/other.wav"
    os.remove(bass_path) if os.path.exists(bass_path) else None
    os.remove(drums_path) if os.path.exists(drums_path) else None
    os.remove(other_path) if os.path.exists(other_path) else None

    demucs_output_dir = f"{output_dir}/demucs" # out/transcribe/album/demucs/htdemucs

    if os.path.exists(f"{text_transcription_dedupe_path}"):
        print(f"Text already transcribed for {audio_file_path}")
        return

    if not os.path.exists(vocals_path):
        demucs(audio_file_path, demucs_output_dir)
    else:
        print(f"Vocals already extracted: {vocals_path}")

    if not os.path.exists(trimmed_path):
        trim_trailing_silence(vocals_path, trimmed_path)
    else:
        print(f"Vocals already trimmed: {trimmed_path}")

    if not os.path.exists(attuned_path):
        attune_for_whisper(trimmed_path, attuned_path)
    else:
        print(f"Vocals already attuned: {attuned_path}")

    # No need to keep this after attuning
    if os.path.exists(attuned_path) and os.path.exists(trimmed_path):
        os.remove(trimmed_path)

    if not os.path.exists(attunedtrim_path):
        trim_trailing_silence(attuned_path, attunedtrim_path)

    if not os.path.exists(f"{text_output_path}"):
        whisper_audio_to_text(attunedtrim_path, text_output_path)

        if not os.path.exists(text_transcription_dedupe_path):
            dedupe_text_transcription(text_transcription_path, text_transcription_dedupe_path)
    else:
        print(f"Text already transcribed: {text_output_path}")
