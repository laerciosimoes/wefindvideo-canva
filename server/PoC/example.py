import os
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
from IPython.display import Video, display

# Função para baixar imagens
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


# Função para gerar narração usando Eleven Labs
def generate_narration(text, voice_id="Xb7hH8MSUJpSbSDYk0k2"):
    API_KEY = "sk_ec96c16d3f21976464df33caf03e6d33707a828ee3142653"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("narration.mp3", "wb") as f:
            f.write(response.content)
    else:
        print(f"Erro ao gerar narração: {response.status_code}")
        print(response.json())
        return False
    return True


# Imagens de cena
scene_images = [
    "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkwNzZ8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjB0ZWNobm9sb2d5JTIwb2ZmaWNlfGVufDB8fHx8MTcyMjU5Njk3MHww&ixlib=rb-4.0.3&q=80&w=1080",
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkwNzZ8MHwxfHNlYXJjaHwxfHxvZmZpY2UlMjBlbXBsb3llZXMlMjB3b3JraW5nJTIwdG9nZXRoZXJ8ZW58MHx8fHwxNzIyNTk2OTcwfDA&ixlib=rb-4.0.3&q=80&w=1080",
    "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkwNzZ8MHwxfHNlYXJjaHwxfHx0ZWNob2xvZ3klMjBjb25zdWx0YW50cyUyMG1lZXRpbmd8ZW58MHx8fHwxNzIyNTk2OTcxfDA&ixlib=rb-4.0.3&q=80&w=1080",
    "https://images.unsplash.com/photo-1680745840784-318be3708374?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkwNzZ8MHwxfHNlYXJjaHwxfHxkaXZlcnNlJTIwaW5kdXN0cnklMjB2aXN1YWxzfGVufDB8fHx8MTcyMjU5NjgwNnww&ixlib=rb-4.0.3&q=80&w=1080",
]

# Dados JSON exemplo (você pode personalizar isso)
json_data = [
    {"description": "Modern technology office", "duration": 3},
    {"description": "Office employees working together", "duration": 3},
    {"description": "Consultants meeting with clients", "duration": 3},
    {"description": "Diverse industry visuals", "duration": 3},
]

def create_video(json_data, scene_images, output_path="video.mp4"):
    clips = []
    narration_texts = []
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

        # Adicionar o texto à lista de narrações
        narration_texts.append(description)

        # Remover arquivo de imagem temporário
        os.remove(image_filename)

    # Concatenar todos os clipes em um único clipe final
    final_clip = concatenate_videoclips(clips, method="compose")

    # Gerar narração para o texto
    full_narration_text = " ".join(narration_texts)
    if generate_narration(full_narration_text):
        if os.path.exists("narration.mp3"):
            audio_clip = AudioFileClip("narration.mp3")
            # Ajustar a duração do vídeo para coincidir com o áudio
            audio_duration = audio_clip.duration
            final_clip = final_clip.subclip(0, min(audio_duration, final_clip.duration))
            # Ajustar a duração do áudio para coincidir com a duração do vídeo
            audio_clip = audio_clip.subclip(0, final_clip.duration)
            # Adicionar a narração ao vídeo
            final_clip = final_clip.set_audio(audio_clip)
        else:
            print(
                "Arquivo de áudio não encontrado. Verifique se a narração foi gerada corretamente."
            )
    else:
        print("Não foi possível gerar a narração.")

    final_clip.write_videofile(output_path, fps=24)

# Criar vídeo
video_output_path = "video.mp4"
create_video(json_data, scene_images, video_output_path)

# Exibir o vídeo no Jupyter Notebook (opcional)
display(Video(video_output_path, embed=True))
