import os
import json
import videoFile

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


import time

load_dotenv()  # take environment variables from .env.
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
unsplash_ID = os.environ["unsplash_ID"]
unsplash_Access_Key = os.environ["unsplash_Access_Key"]
unsplash_Secret_Key = os.environ["unsplash_Secret_Key"]

# print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
# print(f"unsplash_ID: {unsplash_ID}")
# print(f"unsplash_Access_Key: {unsplash_Access_Key}")
# print(f"unsplash_Secret_Key: {unsplash_Secret_Key}")


def getScript(typeVideo, prompt):
    model = ChatOpenAI(model="gpt-4")
    parser = StrOutputParser()
    system_template = """
    Generate a script for a {typeVideo}:
    The should describe each scene in detail, including the setting, characters, and dialogue.
    The result should be a json file with these fields:
    - SceneNumber
    - Title
    - Description
    - Tags
    - VoiceOver
    - Duration
    - QueryImage
    
    The Duration should be in seconds.
    The QueryImage should be a search term for an image that represents the scene.
    Do not include a 'Scene_1', 'Scene_2', etc., as keys for each scene. Each scene should be an item in a list within the JSON object    
    
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
        imageUrls = videoFile.getVideoImages(json_data)
        tmpFile = videoFile.create_video(json_data, imageUrls)
        videoFile.upload_to_blob(tmpFile)
        return { 'script': json_data, 'video_url': f"https://wefindvideo.blob.core.windows.net/video-ai/{tmpFile}" }

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
