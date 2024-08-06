import requests
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
unsplash_Access_Key = os.environ["unsplash_Access_Key"]


def FindImages(query):
    url = "https://api.unsplash.com/search/photos"
    params = {
        'query': query,
        'client_id': unsplash_Access_Key,
        'per_page': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]
        else:
            print(f"No results found for query: {query}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    print(FindImages("cat"))
