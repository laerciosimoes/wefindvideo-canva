import os
import requests
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from IPython.display import Video, display

# Função para baixar imagens
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

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

        # Criar clipe de imagem e texto
        img_clip = ImageClip(image_filename).set_duration(duration)
        txt_clip = (
            TextClip(description, fontsize=24, color="white")
            .set_position("bottom")
            .set_duration(duration)
        )
        video_clip = CompositeVideoClip([img_clip, txt_clip])
        clips.append(video_clip)

        # Remover arquivo de imagem temporário
        os.remove(image_filename)

    # Concatenar todos os clipes em um único clipe final
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24)

# Criar vídeo
video_output_path = "video.mp4"
create_video(json_data, scene_images, video_output_path)

# Exibir o vídeo no Jupyter Notebook
display(Video(video_output_path, embed=True))
