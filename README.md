Click2Flick - Text-to-Video

Click2Flick leverages generative text-to-video technology with advanced API integrations for dynamic content creation.

Overview

This repository contains three main files:
1. image_search.py

    Purpose: Extracts keywords from the user query and searches for relevant images.
    Functionality:
        Uses spaCy to process user input and extract key nouns/proper nouns.
        Queries the Google Custom Search API with refined keywords to retrieve and display the first matching image.

2. video_search.py

    Purpose: Searches for videos based on the user’s query.
    Functionality:
        Uses the Pexels API to find videos relevant to the query.
        Ranks video matches by calculating similarity scores using BERT, identifying the best match.

3. main.py

    Purpose: Combines image search with animation creation, producing a video from the searched image.
    Functionality:
        Calls image_search.py to retrieve an image URL and then sends it to D-ID’s API to generate an animation.
        Monitors the animation’s status with GET requests, providing updates until completion.


Dependencies

   To run these files, install the following libraries:
   1.pip install requests spacy transformers pillow

   Additionally, download the spaCy English model:
   1.python -m spacy download en_core_web_sm

Usage Instructions

1.image_search.py: Run this file to extract keywords and search for images.
2.video_search.py: Run this file to find and rank videos by relevance to the search query.
3.main.py: Use this as the main script to combine image search and animation creation.

