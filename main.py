import base64
import os
import time

import requests

from image_search import search_images


def create_animation(image_url):
    email = os.environ['D_ID_EMAIL']
    api_key = os.environ['D_ID_API_KEY']
    auth = base64.b64encode(f'{email}:{api_key}'.encode()).decode()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth}',
    }

    post_response = requests.post(
        'https://api.d-id.com/animations',
        headers=headers,
        json={
            'source_url': image_url,
            'driver_url': 'bank://classics/driver-country-fire',
            'config': {'mute': False},
        },
    )
    post_response.raise_for_status()
    post_data = post_response.json()

    animation_id = post_data.get('id')
    if not animation_id:
        raise RuntimeError('D-ID did not return an animation id.')

    print('Animation ID:', animation_id)

    get_url = f'https://api.d-id.com/animations/{animation_id}'
    while True:
        get_response = requests.get(get_url, headers=headers)
        get_response.raise_for_status()
        get_data = get_response.json()

        status = get_data.get('status')
        print('Animation status:', status)
        if status != 'started':
            return get_data

        time.sleep(5)


if __name__ == '__main__':
    query = input('Enter image search query: ')
    image_url = search_images(query)

    if image_url is None:
        print('No image results found.')
    else:
        result = create_animation(image_url)
        print(result)
