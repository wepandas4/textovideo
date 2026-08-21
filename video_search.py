import os

import requests
import torch
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer

load_dotenv()

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        _model = AutoModel.from_pretrained('bert-base-uncased')
    return _tokenizer, _model


def _embed(text):
    tokenizer, model = _load_model()
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze(0)


def _similarity(text1, text2):
    a = _embed(text1)
    b = _embed(text2)
    return torch.nn.functional.cosine_similarity(a, b, dim=0).item()


def search_videos(query, per_page=5):
    api_key = os.environ['PEXELS_API_KEY']

    response = requests.get(
        'https://api.pexels.com/videos/search',
        params={'query': query, 'per_page': per_page},
        headers={'Authorization': api_key},
    )
    response.raise_for_status()
    videos = response.json().get('videos')
    if not videos:
        return None

    best_video = max(videos, key=lambda v: _similarity(query, v.get('url', '')))
    return best_video['video_files'][0]['link']


if __name__ == '__main__':
    query = input('Enter video search query: ')
    video_url = search_videos(query)
    print(video_url or 'No video results found.')
