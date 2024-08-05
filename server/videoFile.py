import queryImages
import uuid
import os
import uuid
import requests
from moviepy.editor import (ImageClip,TextClip,ColorClip, CompositeVideoClip, concatenate_videoclips)
from moviepy.video.fx.all import fadein, fadeout
from azure.core.exceptions import ResourceExistsError, AzureError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from moviepy.config import change_settings

load_dotenv()  # take environment variables from .env.

blob_storage_connection_string = os.environ["blob_storage_connection_string"]
#IMAGEMAGICK_BINARY = os.environ["IMAGEMAGICK_BINARY"]
#if IMAGEMAGICK_BINARY:
#    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})


def getVideoImages(jsonData):
    imageUrls = []
    for item in jsonData:
        # print(item)
        imageUrls.append(queryImages.FindImages(item["QueryImage"]))

    # create_video(jsonData, imageUrls, temporary_file_name)
    # return temporary_file_name
    return imageUrls


# Função para baixar imagens
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


# Function to download the file from the URL
# def download_file(url, local_filename):
#    with requests.get(url, stream=True) as r:
#        r.raise_for_status()
#        with open(local_filename, "wb") as f:
#            for chunk in r.iter_content(chunk_size=8192):
#                f.write(chunk)
#    return local_filename


def create_video(json_data, scene_images):
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

    # Concatenar todos os clipes em um único clipe final
    final_clip = concatenate_videoclips(clips, method="compose")
    temporary_file_name = f"video_{uuid.uuid4().hex}.mp4"

    final_clip.write_videofile(temporary_file_name, fps=24)
    return temporary_file_name


# Function to upload the file to Azure Blob Storage
def upload_to_blob(local_filename):

    blob_name = local_filename
    blob_service_client = BlobServiceClient.from_connection_string(blob_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container="video-ai", blob=blob_name)

    try:
        with open(local_filename, "rb") as data:
            blob_client.upload_blob(data)
    except ResourceExistsError:
        print(f"Error: The blob '{blob_client.blob_name}' already exists.")
    except FileNotFoundError:
        print(f"Error: The file '{local_filename}' was not found.")
    except AzureError as e:
        print(f"An error occurred with Azure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    jsonData = [
        {
            "scene_number": 1,
            "Title": "Opening Scene",
            "Description": "Rebeca Andrade and Simone Biles standing at the entrance of a gymnastics stadium, getting ready for their performance. The crowd is cheering in the background.",
            "Tags": ["gymnastics", "Rebeca Andrade", "Simone Biles"],
            "VoiceOver": "Two of the world's most formidable gymnasts, Rebeca Andrade and Simone Biles, prepare for another breathtaking performance",
            "Duration": 10,
            "QueryImage": "Rebeca Andrade and Simone Biles",
        },
        {
            "scene_number": 2,
            "Title": "Rebeca's Performance",
            "Description": "Rebeca Andrade performing her routine on the balance beam. She executes a series of intricate flips and jumps with grace and precision.",
            "Tags": ["Rebeca Andrade", "gymnastics", "performance"],
            "VoiceOver": "Watch as Rebeca Andrade displays her extraordinary talent on the balance beam, a combination of strength, balance, and elegance.",
            "Duration": 15,
            "QueryImage": "Rebeca Andrade balance beam",
        },
        {
            "scene_number": 3,
            "Title": "Simone's Performance",
            "Description": "Simone Biles takes the floor, demonstrating her powerful and dynamic routine. She lands her signature move, 'The Biles', to the amazement of the audience.",
            "Tags": ["Simone Biles", "gymnastics", "performance"],
            "VoiceOver": "Witness the exceptional athleticism of Simone Biles as she performs her iconic move, 'The Biles'.",
            "Duration": 15,
            "QueryImage": "Simone Biles floor routine",
        },
        {
            "scene_number": 4,
            "Title": "Closing Scene",
            "Description": "Rebeca and Simone embrace after their performances. The crowd stands, clapping and cheering, acknowledging the extraordinary talent of these two athletes.",
            "Tags": ["Rebeca Andrade", "Simone Biles", "gymnastics"],
            "VoiceOver": "The crowd roars in appreciation for these two remarkable athletes, Rebeca Andrade and Simone Biles, as they wrap up their performances.",
            "Duration": 10,
            "QueryImage": "Rebeca Andrade and Simone Biles hugging",
        },
    ]

    imageUrls = getVideoImages(jsonData)
    fileName = create_video(jsonData, imageUrls)
    print(fileName)
