import requests
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

unsplash_Access_Key = os.environ["unsplash_Access_Key"]

def FindImages(query):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplash_Access_Key}&per_page=1"
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["urls"]["regular"]
    # images = [result["urls"]["regular"] for result in data["results"]]
    # return images[0]


if __name__ == "__main__":
    print(FindImages("cat"))