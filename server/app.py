import videoFile
import voiceVideo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import videoScript
import videoMusic


class VideoRequest(BaseModel):
    prompt: str
    videoType: str


# 4. App definition
app = FastAPI(
    title="WeFindVideo Server",
    version="1.0",
    description="WeFindVideo API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict to specific origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # Allow all headers
)

# 5. Adding generate-video route
@app.post("/generate-video/")
def generate_video(request: VideoRequest):
    try:
        json_data = videoScript.get_json_data(request.videoType, request.prompt)
        imageUrls = videoFile.getVideoImages(json_data)
        tmp_AudioFile = voiceVideo.create_audio(json_data)
        musicFile = videoMusic.getMusic(json_data)
        tmp_VideoFile = videoFile.create_video(json_data, imageUrls, tmp_AudioFile, musicFile)
        videoUrl = videoFile.upload_to_blob(tmp_VideoFile)
        voiceVideo.Dispose(tmp_AudioFile)
        videoFile.Dispose(tmp_VideoFile)

        return {
            "script": json_data,
            "video_url": videoUrl,
        }
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
