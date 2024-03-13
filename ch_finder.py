# youtube_api.py
# YouTube API를 사용하여 채널 ID를 가져오는 함수들을 포함하는 파일입니다.
from googleapiclient.discovery import build

def initialize_youtube_api(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_id(youtube, artist_name):
    search_response = youtube.search().list(
        q=artist_name,
        part='snippet',
        type='channel',
        maxResults=1
    ).execute()
    
    if search_response['items']:
        return search_response['items'][0]['id']['channelId']
    else:
        return None
