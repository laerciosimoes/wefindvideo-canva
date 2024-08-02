import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI


load_dotenv()  # take environment variables from .env.

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
