from googleapiclient.discovery import build
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time, subprocess
import os

# YouTube Data API 초기화 및 채널 ID 가져오기
def initialize_youtube_api(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_id(youtube, artist_name):
    response = youtube.search().list(q=artist_name, part='snippet', type='channel', maxResults=1).execute()
    if response['items']:
        return response['items'][0]['id']['channelId']
    return None

# Selenium을 사용하여 채널의 재생목록 링크 가져오기
def get_youtube_playlist_links(channel_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(channel_url)
    time.sleep(5)  # 동적 콘텐츠 로드를 위한 대기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    found_hrefs = set()
    for element in soup.find_all(class_='style-scope ytd-rich-grid-media'):
        a_tag = element.find_parent('a')
        if a_tag and (href := a_tag.get('href')):
            full_url = f"https://www.youtube.com{href}"
            found_hrefs.add(full_url)
    return found_hrefs

# youtube-dl을 사용하여 재생목록의 비디오 다운로드
def download_playlist_videos(playlist_urls, download_path):
    # 저장될 파일 경로 및 파일명 형식 지정
    for url in playlist_urls:
        output_template = os.path.join(download_path, '%(title)s.%(ext)s')
        # youtube-dl 명령어 구성
        command = [
            'youtube-dl',
            '--extract-audio',  # 오디오 추출
            '--audio-format', 'mp3',  # 오디오 포맷을 mp3로 지정
            '--output', output_template,  # 출력 파일 경로 및 이름 형식 지정
            #youtube_url  # 다운로드할 YouTube 비디오 URL
        ]
        
        subprocess.run([
            'youtube-dl',
            '-o', f'{download_path}/%(title)s.%(ext)s',
            url
        ])

if __name__ == "__main__":
    API_KEY = 'AIzaSyCs6dodjKFWh2smPMUs9FkiGPU0FxyUR44'
    artist_name = 'GIDLE'
    download_path = r'C:\Users\SCHOOL\Desktop\music'
    
    youtube = initialize_youtube_api(API_KEY)
    channel_id = get_channel_id(youtube, artist_name)
    if channel_id:
        channel_url = f"https://www.youtube.com/channel/{channel_id}/releases"
        playlist_urls = get_youtube_playlist_links(channel_url)
        download_playlist_videos(playlist_urls, download_path)
        print(f"Download completed for {artist_name}")
    else:
        print("Channel not found.")
