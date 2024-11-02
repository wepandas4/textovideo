import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Set the search query and number of videos to retrieve
q = 'smiling woman'  # Example search query
per_page = 5  # Number of videos to retrieve

# Set the API URL
url = f"https://api.pexels.com/videos/search?query={q}&per_page={per_page}"

# Set the request headers with your API key
headers = {
    'Authorization': 'YOUR_API_KEY',
}

# Send the GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON response
    data = response.json()

    # Check if videos were found in the response
    if 'videos' in data and len(data['videos']) > 0:
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

        # Calculate the similarity score for each video and the reference text
        similarity_scores = []
        for video in data['videos']:
            video_title = video['user']['name'] + ' ' + video['video_files'][0]['link']
            similarity_score = calculate_similarity(reference_text, video_title)
            similarity_scores.append(similarity_score)

        # Find the index of the video with the highest similarity score
        best_index = max(range(len(similarity_scores)), key=similarity_scores.__getitem__)

        # Get the URL of the best-matching video
        best_video_url = data['videos'][best_index]['video_files'][0]['link']
        print("Best Video URL:", best_video_url)
    else:
        print("No videos found for the search query.")
else:
    print("Request failed with status code:", response.status_code)
