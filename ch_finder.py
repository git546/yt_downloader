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

def get_uploads_playlist_id(youtube, channel_id):
    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    
    if channel_response['items']:
        return channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        return None

def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    next_page_token = None
    
    while True:
        playlist_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=5,
            pageToken=next_page_token
        ).execute()
        
        videos.extend(playlist_response['items'])
        
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def main(api_key, artist_name):
    youtube = initialize_youtube_api(api_key)
    
    # 아티스트의 채널 ID 가져오기
    channel_id = get_channel_id(youtube, artist_name)
    if not channel_id:
        print("Channel not found.")
        return
    
    # 채널의 업로드 재생목록 ID 가져오기
    uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
    if not uploads_playlist_id:
        print("Uploads playlist not found.")
        return
    
    # 업로드 재생목록에서 비디오 목록 가져오기
    videos = get_videos_from_playlist(youtube, uploads_playlist_id)
    
    # 비디오 목록 출력
    for video in videos:
        print(video['snippet']['title'], video['snippet']['resourceId']['videoId'])

# 사용 예시
api_key = 'AIzaSyCs6dodjKFWh2smPMUs9FkiGPU0FxyUR44'  # 여기에 실제 API 키를 입력하세요.
artist_name = '르세라핌'  # 여기에 검색하고자 하는 아티스트 이름을 입력하세요.
main(api_key, artist_name)

