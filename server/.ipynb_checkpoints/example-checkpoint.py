import json
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from IPython.display import Video, display

# Sample JSON data
json_data = [
    {"description": "Our Success Stories\nThrough our dedication to excellence...", "duration": 5},
    {"description": "Why HPC BRASIL?\nChoosing HPC BRASIL means partnering with...", "duration": 5},
    {"description": "Our Promise\nAt HPC BRASIL, we promise to deliver innovative...", "duration": 5},
    {"description": "Closing Scene\n[Visuals of the HPC BRASIL team working collaboratively...]", "duration": 5},
    {"description": 'Voiceover: "Get in touch with HPC BRASIL today..."', "duration": 5},
]

# Sample scene images
scene_images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
    "https://example.com/image4.jpg",
    "https://example.com/image5.jpg",
]

def create_video(json_data, scene_images, output_path="video.mp4"):
    clips = []
    for scene, image_url in zip(json_data, scene_images):
        duration = int(scene["duration"])
        if image_url:
            img_clip = ImageClip(image_url).set_duration(duration)
            txt_clip = (
                TextClip(scene["description"], fontsize=24, color="white")
                .set_position("bottom")
                .set_duration(duration)
            )
            video_clip = CompositeVideoClip([img_clip, txt_clip])
            clips.append(video_clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24)

# Create the video
video_output_path = "video.mp4"
create_video(json_data, scene_images, video_output_path)

# Display the video in the Jupyter Notebook
display(Video(video_output_path, embed=True))
