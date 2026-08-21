# Click2Flick - Text-to-Video

Click2Flick leverages generative text-to-video technology with advanced API integrations for dynamic content creation.

## What it does

- `image_search.py`: extracts keywords from a query with spaCy, searches
  Google Custom Search for a matching image, and returns the top result.
- `video_search.py`: searches Pexels for videos matching a query, then
  ranks candidates by cosine similarity between BERT embeddings of the
  query and each video's title, returning the best match.
- `main.py`: the end-to-end pipeline. Takes a query, finds an image with
  `image_search.py`, then sends it to D-ID's API to animate it, polling
  until the animation is ready.

## How to use it

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
```

Fill in `.env` with your own keys:

- `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`: Google Custom Search
- `PEXELS_API_KEY`: Pexels
- `D_ID_EMAIL` and `D_ID_API_KEY`: D-ID

Then run any of the three scripts directly:

```bash
python main.py
python image_search.py
python video_search.py
```

## About the Team

This project was developed by our dedicated team. We are proud of our collective efforts and the innovative solutions we've created!

| Team Member         | GitHub Profile                                           | Email                        |
|---------------------|----------------------------------------------------------|------------------------------|
| **Priyanka M K**    | [Priyaaaa2](https://github.com/Priyaaaa2)                | priyankamk2903@gmail.com     |
| **Sumukh C**        | [Sumu004](https://github.com/Sumu004)                    | sumukhchaluvaraj@gmail.com   |
| **Ravi J Gowda**    | [RaviGowda29](https://github.com/RaviGowda29)            | ravigowdaedu29@gmail.com     |
| **Yashwanth M**     | [yashwanthm3012](https://github.com/yashwanthm3012)      | dev.yashwanthm3012@gmail.com |

We appreciate the hard work and collaboration that made this project possible!
