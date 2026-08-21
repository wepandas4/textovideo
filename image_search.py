import os

import requests
import spacy
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load('en_core_web_sm')


def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN')]


def search_images(query):
    api_key = os.environ['GOOGLE_API_KEY']
    cse_id = os.environ['GOOGLE_CSE_ID']

    keywords = extract_keywords(query)
    search_query = ' '.join(keywords) or query

    params = {
        'key': api_key,
        'cx': cse_id,
        'q': search_query,
        'searchType': 'image',
    }

    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
    response.raise_for_status()
    results = response.json()

    items = results.get('items')
    if not items:
        return None

    return items[0]['link']


if __name__ == '__main__':
    query = input('Enter image search query: ')
    image_url = search_images(query)
    print(image_url or 'No image results found.')
