import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import requests
from moviepy.editor import ImageClip, TextClip, ColorClip, CompositeVideoClip
from moviepy.video.fx  import fadein, fadeout
import time

load_dotenv()  # take environment variables from .env.
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
unsplash_ID = os.environ["unsplash_ID"]
unsplash_Access_Key = os.environ["unsplash_Access_Key"]
unsplash_Secret_Key = os.environ["unsplash_Secret_Key"]

print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
print(f"unsplash_ID: {unsplash_ID}")
print(f"unsplash_Access_Key: {unsplash_Access_Key}")
print(f"unsplash_Secret_Key: {unsplash_Secret_Key}")


# Função para baixar imagens
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


def create_video(json_data, scene_images, output_path="video.mp4"):
    clips = []
    for scene, image_url in zip(json_data, scene_images):
        duration = scene.get("duration")
        description = scene.get("description", "")

        # Verificar se a duração e a URL da imagem são válidas
        if duration is None:
            raise ValueError("A duração não pode ser None")
        duration = int(duration)
        if not image_url:
            raise ValueError("URL da imagem não pode ser None")

        # Nome do arquivo de imagem temporário
        image_filename = f"temp_image.jpg"
        # Baixar imagem
        download_image(image_url, image_filename)

        # Criar clipe de imagem
        img_clip = ImageClip(image_filename).set_duration(duration)

        # Criar clipe de texto
        txt_clip = TextClip(
            description, fontsize=24, color="white", bg_color="black", size=(None, None)
        )
        txt_clip = txt_clip.set_duration(duration).set_position(("center", "bottom"))

        # Ajustar o tamanho do fundo com base no texto
        text_size = txt_clip.size
        background_clip = (
            ColorClip(size=(text_size[0] + 20, text_size[1] + 10), color=(0, 0, 0))
            .set_duration(duration)
            .set_opacity(0.5)
            .set_position(("center", "bottom"))
        )

        # Criar o clipe final combinando imagem, fundo e texto
        video_clip = CompositeVideoClip([img_clip, background_clip, txt_clip])

        # Aplicar efeitos de fade-in e fade-out
        video_clip = video_clip.fx(fadein, duration=1).fx(
            fadeout, duration=1
        )  # 1 segundo para fade-in e fade-out
        clips.append(video_clip)

        # Remover arquivo de imagem temporário
        os.remove(image_filename)




def getScript(typeVideo, prompt):
    model = ChatOpenAI(model="gpt-4")
    parser = StrOutputParser()
    system_template = """
    Generate a script for a {typeVideo}:
    The should describe each scene in detail, including the setting, characters, and dialogue.
    The result should be a json file with these fiedls:
    - scene_number
    - Title
    - Description
    - Tags
    - VoiceOver
    - Duration
    - QueryImage
    
    The Duration should be in seconds.
    The QueryImage should be a search term for an image that represents the scene.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    chain = prompt_template | model | parser

    result = chain.invoke({"typeVideo": typeVideo, "text": prompt})
    return result


class VideoRequest(BaseModel):
    prompt: str
    videoType: str


# 4. App definition
app = FastAPI(
    title="WeFindVideo Server",
    version="1.0",
    description="WeFindVideo API",
)


def get_json_data_with_retries(prompt, subject, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = getScript(prompt, subject)
            json_data = json.loads(response)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1}: Invalid JSON data received. Error: {e}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: An error occurred. Error: {e}")

        # Wait for a short period before retrying
        time.sleep(2)

    raise ValueError("Failed to get valid JSON data after multiple attempts.")


# 5. Adding generate-video route
@app.post("/generate-video/")
def generate_video(request: VideoRequest):
    try:
        json_data = get_json_data_with_retries(request.videoType, request.prompt)

        video_file = getVideoFile(json_data)
        return json_data

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
