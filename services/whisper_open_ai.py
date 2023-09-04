import whisper


def speech_to_text(audio_path: str):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result
