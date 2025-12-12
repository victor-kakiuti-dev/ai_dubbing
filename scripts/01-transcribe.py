from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_path = "../output/audio_original.wav"

with open(audio_path, "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",  # Mude para whisper-1
        file=f,
        response_format="verbose_json",  # Adicione este parâmetro
        timestamp_granularities=["segment"],  # Timestamps por palavra e segmento
        temperature=0
    )

transcript_dict = transcript.model_dump()


with open("timestamps.json", "w", encoding="utf-8") as f:
    json.dump(transcript_dict, f, indent=2, ensure_ascii=False)

print("Salvo como JSON: timestamps.json")

