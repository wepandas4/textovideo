import requests
import json
import PIL.Image as Image
from io import BytesIO
import time
import spacy

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract the keywords (nouns and proper nouns)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    return keywords

def search_images(query):
    api_key = 'YOUR_API_KEY'  # Replace with your API key
    cse_id = 'YOUR_CXID'  # Replace with your Custom Search Engine ID

    keywords = extract_keywords(query)
    search_query = ' '.join(keywords)

    url = f'https://www.googleapis.com/customsearch/v1?cx={cse_id}&key={api_key}&q={search_query}&searchType=image'

    response = requests.get(url)
    results = json.loads(response.text)

    if 'items' in results:
        item = results['items'][0]  # Get the first image result
        print('Title:', item['title'])
        print('Link:', item['link'])
        print('Image Preview:')

        image_url = item['link']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image.show()
        print('---')
        return image_url  # Return the image URL
    else:
        print('No image results found.')
        return None


query = input("Enter image search query: ")
image_url = search_images(query)

if image_url is not None:
    # POST request
    post_url = "https://api.d-id.com/animations"
    post_payload = json.dumps({
        "source_url": image_url,
        "driver_url": "bank://classics/driver-country-fire",
        "config": {
            "mute": False
        }
    })
    post_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YOUR_DID_API_KEY'
    }
    post_response = requests.post(post_url, headers=post_headers, data=post_payload)
    post_data = post_response.json()

    if 'id' in post_data:
        animation_id = post_data['id']
        print("POST Request successful. Animation ID:", animation_id)
        print()

        # GET request
        get_url = "https://api.d-id.com/animations/{}".format(animation_id)
        get_payload = {}
        get_headers = {
            'Authorization': 'Basic YOUR_DID_API_KEY'
        }

        # Check animation status until it is no longer "started"
        while True:
            get_response = requests.get(get_url, headers=get_headers, data=get_payload)
            get_data = get_response.json()

            if 'status' in get_data and get_data['status'] != 'started':
                break

            print("Animation status: ", get_data['status'])
            time.sleep(5)  # Wait for 5 seconds before checking again

        print("Animation status: ", get_data['status'])
        print("GET Response:")
        print(get_response.text)
    else:
        print("POST Request failed. Unable to retrieve Animation ID.")
