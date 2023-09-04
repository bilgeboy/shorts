from config import eleven_labs_api_key
from elevenlabs import set_api_key, generate


def get_audio_bytes(text: str):
    set_api_key(eleven_labs_api_key)
    audio = generate(
        text=text,
        voice='James',
        model="eleven_monolingual_v1"
    )

    return audio
