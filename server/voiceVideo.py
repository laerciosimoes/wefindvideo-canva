import os
import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()  # take environment variables from .env.
ELEVEN_API_KEY = os.environ["ELEVEN_API_KEY"]


# Função para gerar narração usando Eleven Labs
def generate_narration(text, voice_id="Xb7hH8MSUJpSbSDYk0k2"):
    API_KEY = ELEVEN_API_KEY
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:

        temp_audio_name = f"audio_{uuid.uuid4().hex}.mp3"
        with open(temp_audio_name, "wb") as f:
            f.write(response.content)
        return temp_audio_name
    else:
        print(f"Erro ao gerar narração: {response.status_code}")
        print(response.json())
        return None


def Dispose(audioFile):
    os.remove(audioFile)


def create_audio(json_data):
    narration_texts = []

    for scene in json_data:
        print(scene)
        description = scene.get("VoiceOver")
        # Adicionar o texto à lista de narrações
        narration_texts.append(description)

    # Gerar narração para o texto
    full_narration_text = " ".join(narration_texts)

    return generate_narration(full_narration_text)

