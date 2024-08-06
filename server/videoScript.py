from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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


def get_json_data(prompt, subject, max_retries=3):
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
