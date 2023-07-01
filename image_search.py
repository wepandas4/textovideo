import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Set the search query and number of images to retrieve
q = 'ronaldo and messi'  # Example search query
num_images = 5  # Number of images to retrieve

# Set the API URL
url = "https://www.googleapis.com/customsearch/v1"

# Set the request parameters including your API key and custom search engine ID
params = {
    "key": "AIzaSyD6ZkQGu8yecrMsDYeD1WA-1DL1-7EKY4w",
    "cx": "f0047a0ee6fcc4725",
    "q": q,
    "num": num_images,
    "searchType": "image"
}

# Send the GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON response
    data = response.json()

    # Check if images were found in the response
    if 'items' in data and len(data['items']) > 0:
        # Initialize BERT tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

        # Define a function to calculate the text-image similarity score
        def calculate_similarity(text1, text2):
            encoded_inputs = tokenizer(text1, text2, padding=True, truncation=True, return_tensors='pt')
            outputs = model(**encoded_inputs)
            logits = outputs.logits
            similarity_score = logits.softmax(dim=1)[:, 1].item()
            return similarity_score

        # Define the reference text
        reference_text = 'A happy woman smiling'

        # Calculate the similarity score for each image and the reference text
        similarity_scores = []
        for item in data['items']:
            image_title = item['title'] + ' ' + item['link']
            similarity_score = calculate_similarity(reference_text, image_title)
            similarity_scores.append(similarity_score)

        # Find the index of the image with the highest similarity score
        best_index = max(range(len(similarity_scores)), key=similarity_scores.__getitem__)

        # Get the URL of the best-matching image
        best_image_url = data['items'][best_index]['link']
        print("Best Image URL:", best_image_url)
    else:
        print("No images found for the search query.")
else:
    print("Request failed with status code:", response.status_code)
