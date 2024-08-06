import videoImages
import uuid
import os
import uuid
import requests
from moviepy.editor import (
    ImageClip,
    TextClip,
    ColorClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip,
)
from moviepy.video.fx.all import fadein, fadeout
from azure.core.exceptions import ResourceExistsError, AzureError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from moviepy.config import change_settings

load_dotenv()  # take environment variables from .env.

blob_storage_connection_string = os.environ.get("blob_storage_connection_string")
IMAGEMAGICK_BINARY = os.environ.get("IMAGEMAGICK_BINARY")

if not blob_storage_connection_string:
    raise EnvironmentError(
        "Required environment variable 'blob_storage_connection_string' is not set."
    )

if IMAGEMAGICK_BINARY:
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})

# Set the default font to a font that is known to be available
os.environ["MAGICK_FONT"] = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def getVideoImages(jsonData):
    imageUrls = []
    for item in jsonData:
        print(item)
        imageUrls.append(videoImages.FindImages(item.get("QueryImage")))
    return imageUrls


# Função para baixar imagens
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


def create_video(json_data, scene_images,audio_file):
    clips = []

    for scene, image_url in zip(json_data, scene_images):
        duration = scene["Duration"]
        description = scene["Description"]

        # Verificar se a duração e a URL da imagem são válidas
        if duration is None:
            raise ValueError("A duração não pode ser None")
        duration = int(duration)
        if not image_url:
            raise ValueError("URL da imagem não pode ser None")

        # Nome do arquivo de imagem temporário
        image_filename = f"image_{uuid.uuid4().hex}.jpg"
        # Baixar imagem
        download_image(image_url, image_filename)

        # Criar clipe de imagem
        img_clip = ImageClip(image_filename).set_duration(duration)

        # print(f"Listing Fonts {TextClip.list('font')}")

        # Criar clipe de texto
        txt_clip = TextClip(
            description, font='DejaVu-Sans', fontsize=24, color="white", bg_color="black", size=(None, None)
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

    # Concatenar todos os clipes em um único clipe final
    final_clip = concatenate_videoclips(clips, method="compose")

    if audio_file:
        audio_clip = AudioFileClip(audio_file)
        # Ajustar a duração do vídeo para coincidir com o áudio
        audio_duration = audio_clip.duration
        final_clip = final_clip.subclip(0, min(audio_duration, final_clip.duration))
        # Ajustar a duração do áudio para coincidir com a duração do vídeo
        audio_clip = audio_clip.subclip(0, final_clip.duration)
        # Adicionar a narração ao vídeo
        final_clip = final_clip.set_audio(audio_clip)

    temp_video_name = f"video_{uuid.uuid4().hex}.mp4"

    final_clip.write_videofile(temp_video_name, fps=24, codec="libx264")
    return temp_video_name


def Dispose(videoFile):
    os.remove(videoFile)

# Function to upload the file to Azure Blob Storage
def upload_to_blob(local_filename):

    blob_name = local_filename
    blob_service_client = BlobServiceClient.from_connection_string(blob_storage_connection_string)

    try:
        blob_client = blob_service_client.get_blob_client(container="video-ai", blob=blob_name)

        with open(local_filename, "rb") as data:
            blob_client.upload_blob(data)
        return blob_client.url
    except ResourceExistsError:
        return f"Error: The blob '{blob_client.blob_name}' already exists."
    except FileNotFoundError:
        return f"Error: The file '{local_filename}' was not found."
    except AzureError as e:
        return f"An error occurred with Azure: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
