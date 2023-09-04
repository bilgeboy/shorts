import logging
from enum import Enum
import requests
from config import pexels_api_key

headers = {"Authorization": pexels_api_key}
BASE_URL = 'https://api.pexels.com'


class VideoSize(Enum):
    Small = 'small'
    Medium = 'medium'
    Large = 'large'


class VideoOrientation(Enum):
    Landscape = 'landscape'
    Portrait = 'portrait'
    Square = 'square'


def search_videos(query: str, page: int, orientation: VideoOrientation, video_size: VideoSize = VideoSize.Small):
    """
    https://www.pexels.com/api/documentation/?#videos-search
    """
    payload = {
        'query': query,
        'page': page,
        'per_page': 15,  # Max 80
        'locale': 'en-US',
        'size': video_size.value,
        'orientation': orientation.value
    }

    response = requests.get(f'{BASE_URL}/videos/search', params=payload, headers=headers)
    return response.json()


def get_video_bytes(key_word: str):
    logging.info('getting video')
    videos_data = search_videos(key_word, 1, VideoOrientation.Portrait)
    videos = videos_data.get('videos', [])
    if videos == []:
        return None
    logging.info('downloading video')
    video_files = videos[0].get('video_files', [])
    for file in video_files:
        if 2500 > file['height'] >= 1920:
            print(file)
            response = requests.get(file['link'])
            return response.content

    return None
