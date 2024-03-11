
from googleapiclient.discovery import build
from pytube import YouTube
from moviepy.editor import *
import html
import os

def initialize_youtube_api(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def search_videos(youtube, query, max_results=50):
    request = youtube.search().list(q=query, part='snippet', type='video', maxResults=max_results)
    return request.execute()

def get_video_category(youtube, video_id):
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    if response['items']:
        return response['items'][0]['snippet']['categoryId']
    else:
        return None
 
def existing_files(save_path):
    return {f.replace('.mp3', '') for f in os.listdir(save_path) if f.endswith('.mp3')}

def download_video_as_mp3(youtube, video, save_path):
    video_id = video['id']['videoId']
    # HTML 엔티티를 해당 문자로 변환
    video_title = html.unescape(video['snippet']['title']).replace('/', '-')
    # 파일명에서 특수 문자 제거 또는 변환 로직 추가
    video_title = video_title.replace('&#39;', "'")

    # 기존 파일 확인 로직 추가
    save_file_path = os.path.join(save_path, f"{video_title}.mp3")
    if os.path.exists(save_file_path):
        print(f"File already exists: {save_file_path}")
        return
        video_id = video['id']['videoId']
        video_title = video['snippet']['title'].replace('/', '-')
        save_file_path = os.path.join(save_path, f"{video_title}.mp3")
    
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        stream = yt.streams.filter(only_audio=True).first()
        download_path = stream.download(output_path=save_path, filename=f"{video_title}.mp4")
        
        clip = AudioFileClip(download_path)
        clip.write_audiofile(save_file_path)
        clip.close()
        os.remove(download_path)  # Remove the downloaded .mp4 file
        
        print(f"Downloaded and converted to MP3: {save_file_path}")
    except Exception as e:
        print(f"Failed to download {video_title}: {e}")

def filter_and_download_videos(api_key, query, save_path, max_downloads=5):
    youtube = initialize_youtube_api(api_key)
    search_response = search_videos(youtube, query)
    videos = search_response.get('items', [])
    existing_titles = existing_files(save_path)
    
    downloads_count = 0
    for video in videos:
        if downloads_count >= max_downloads:
            break
        
        video_title = video['snippet']['title']
        if video_title in existing_titles:
            continue  # Skip existing files
        
        video_id = video['id']['videoId']
        category_id = get_video_category(youtube, video_id)
        if category_id == '10':  # '음악' 카테고리
            download_video_as_mp3(youtube, video, save_path)
            downloads_count += 1

# 사용 예
api_key = ''  # API 키
query = 'music'  # 검색 쿼리
save_path = r'C:\Users\오상윤\Desktop\티스토리 용'  # 저장 경로
filter_and_download_videos(api_key, query, save_path)


