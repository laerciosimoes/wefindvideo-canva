import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import subprocess

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
unsplash_ID = os.environ["unsplash_ID"]
unsplash_Access_Key = os.environ["unsplash_Access_Key"]
unsplash_Secret_Key = os.environ["unsplash_Secret_Key"]

def getScript(typeVideo, prompt):
    model = ChatOpenAI(model="gpt-4")
    parser = StrOutputParser()
    system_template = """
    Generate a script for a {typeVideo}:
    The should describe each scene in detail, including the setting, characters, and dialogue.
    The result should be a json file with these fields:
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

def create_video_from_json(json_data, output_path="video.mp4"):
    # Save JSON data to a file
    with open("scene_data.json", "w") as f:
        json.dump(json_data, f)

    # Run the script that creates the video
    subprocess.run(["python", "example.py"], check=True)
    
    # Move the output file to the desired location
    os.rename("video.mp4", output_path)
    
    return output_path

class VideoRequest(BaseModel):
    prompt: str
    videoType: str

app = FastAPI(
    title="WeFindVideo Server",
    version="1.0",
    description="WeFindVideo API",
)

@app.post("/generate-video/")
def generate_video(request: VideoRequest):
    try:
        script_data = getScript(request.videoType, request.prompt)
        video_file = create_video_from_json(script_data, "generated_video.mp4")
        return {"videoUrl": video_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
