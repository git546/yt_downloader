import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import ch_finder  # ch_finder.py 모듈을 import 합니다.

# YouTube API 키를 여기에 입력하세요.
API_KEY = 'AIzaSyCs6dodjKFWh2smPMUs9FkiGPU0FxyUR44'

def on_entry_click(event):
    """Entry 위젯 클릭 시 실행되는 함수"""
    if entry_artist_name.get() == '가수/아티스트 입력':
        entry_artist_name.delete(0, "end")  # 텍스트 삭제
        entry_artist_name.insert(0, '')  # 빈 텍스트 삽입
        entry_artist_name.config(fg='black')

def on_focusout(event):
    """Entry 위젯이 포커스를 잃었을 때 실행되는 함수"""
    if entry_artist_name.get() == '':
        entry_artist_name.insert(0, '가수/아티스트 입력')
        entry_artist_name.config(fg='grey')

def async_download(artist_name):
    youtube = ch_finder.initialize_youtube_api(API_KEY)
    channel_id = ch_finder.get_channel_id(youtube, artist_name)
    
    if channel_id:
        # 여기서는 채널 ID를 표시하기만 합니다. 실제 다운로드 로직이 필요한 경우 추가해야 합니다.
        text = f"찾은 채널 ID: {channel_id}"
    else:
        text = "채널을 찾을 수 없습니다."
    
    # GUI 요소에 접근하기 위해 메인 스레드에서 실행되어야 합니다.
    label_status.config(text=text)
    entry_artist_name.config(state=tk.NORMAL)
    button_download.config(state=tk.NORMAL)

def download():
    artist_name = entry_artist_name.get()
    if not artist_name or artist_name == "가수/아티스트 입력":
        messagebox.showinfo("알림", "가수/아티스트 이름을 입력해주세요.")
        return
    
    entry_artist_name.config(state=tk.DISABLED)
    button_download.config(state=tk.DISABLED)
    label_status.config(text="검색 중...")
    
    # 비동기적으로 YouTube 채널 ID를 검색합니다.
    threading.Thread(target=async_download, args=(artist_name,)).start()

def open_folder():
    pass  # 폴더 열기 로직

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

button_download = tk.Button(root, text="채널 검색", command=download)
button_download.pack(pady=5)

button_open = tk.Button(root, text="열기", command=open_folder)
button_open.pack(pady=5)

button_set_path = tk.Button(root, text="경로 지정", command=set_download_path)
button_set_path.pack(pady=5)

root.mainloop()
