import asyncio
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import ch_finder  # ch_finder.py 모듈을 import 합니다.
import list_maker # list_make.py 모듈을 import 합니다.
import time

# YouTube API 키를 여기에 입력하세요.
API_KEY = 'AIzaSyCs6dodjKFWh2smPMUs9FkiGPU0FxyUR44'

# 전역 변수로 검색된 채널의 이름과 ID를 저장
channel_name = ""
channel_id = ""

async def get_links(channel_id):
    playlist_links = await list_maker.get_lists_async(channel_id)
    return playlist_links

def on_entry_click(event):
    global channel_name, channel_id
    if entry_artist_name.get() == '가수/아티스트 입력':
        entry_artist_name.delete(0, "end")
        entry_artist_name.insert(0, '')
        entry_artist_name.config(fg='black')
    channel_name = ""
    channel_id = ""

def on_focusout(event):
    if entry_artist_name.get() == '':
        entry_artist_name.insert(0, '가수/아티스트 입력')
        entry_artist_name.config(fg='grey')

def async_search_channel(artist_name):
    global channel_name, channel_id
    youtube = ch_finder.initialize_youtube_api(API_KEY)
    channel_info = ch_finder.get_channel_id(youtube, artist_name)
    
    if channel_info:
        channel_id = channel_info
        # 검색된 채널의 이름도 얻기 위해 추가 정보 요청
        channel_details = youtube.channels().list(id=channel_id, part='snippet').execute()
        channel_name = channel_details['items'][0]['snippet']['title']
        text = f"찾은 채널: {channel_name}"
    else:
        text = "채널을 찾을 수 없습니다."
        channel_id = ""
    
    label_status.config(text=text)
    entry_artist_name.config(state=tk.NORMAL)
    button_search.config(state=tk.NORMAL)

def search_channel():
    artist_name = entry_artist_name.get()
    if not artist_name or artist_name == "가수/아티스트 입력":
        messagebox.showinfo("알림", "가수/아티스트 이름을 입력해주세요.")
        return
    
    entry_artist_name.config(state=tk.DISABLED)
    button_search.config(state=tk.DISABLED)
    label_status.config(text="검색 중...")
    
    threading.Thread(target=async_search_channel, args=(artist_name,)).start()

def download_videos():
    if not channel_id:
        messagebox.showinfo("알림", "먼저 채널을 검색해주세요.")
        return
    # 여기에 채널 비디오 다운로드 로직 구현
    playlist_list = asyncio.run(get_links)
    print(playlist_list)
    messagebox.showinfo("알림", f"'{channel_name}' 채널의 비디오를 다운로드합니다.")

def open_folder():
    pass

def set_download_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        label_status.config(text=f"다운로드 경로: {folder_selected}")
    else:
        label_status.config(text="다운로드 경로가 지정되지 않았습니다.")

root = tk.Tk()
root.title("YouTube Channel Finder")

entry_artist_name = tk.Entry(root, fg='grey', width=50)
entry_artist_name.pack(pady=10)
entry_artist_name.insert(0, '가수/아티스트 입력')
entry_artist_name.bind('<FocusIn>', on_entry_click)
entry_artist_name.bind('<FocusOut>', on_focusout)

label_status = tk.Label(root, text="")
label_status.pack(pady=10)

button_search = tk.Button(root, text="채널 검색", command=search_channel)
button_search.pack(pady=5)

button_download = tk.Button(root, text="비디오 다운로드", command=download_videos)
button_download.pack(pady=5)

button_open = tk.Button(root, text="열기", command=open_folder)
button_open.pack(pady=5)

button_set_path = tk.Button(root, text="경로 지정", command=set_download_path)
button_set_path.pack(pady=5)

root.mainloop()
