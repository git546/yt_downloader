from googleapiclient.discovery import build

def initialize_youtube_api(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def search_artist_channel(api_key, artist_name):
    youtube = initialize_youtube_api(api_key)
    request = youtube.search().list(
        q=artist_name,
        part='snippet',
        type='channel',
        maxResults=5
    )
    response = request.execute()

    # 검색 결과 중 가장 관련성 높은 채널 선택
    for item in response.get('items', []):
        # 여기서는 단순히 첫 번째 채널을 선택하지만,
        # 필요에 따라 채널의 구독자 수나 다른 메타데이터를 활용하여 선택할 수 있습니다.
        channel_id = item['id']['channelId']
        channel_title = item['snippet']['title']
        print(f"Found channel: {channel_title}, Channel ID: {channel_id}")
        break  # 가장 첫 번째 결과만 사용

# 사용 예시
api_key = 'YOUR_API_KEY'  # 여기에 실제 API 키를 입력하세요.
artist_name = '아티스트 이름'  # 여기에 검색하고자 하는 아티스트 이름을 입력하세요.
search_artist_channel(api_key, artist_name)
