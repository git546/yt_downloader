from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time

# Selenium 웹드라이버 초기화 (Chrome 사용 예시)
chrome_options = Options()
driver = webdriver.Chrome('./chromedriver', options=chrome_options)

# 유튜브 아티스트 채널 또는 앨범 목록 페이지로 이동
driver.get('https://www.youtube.com/channel/UCs-QBT4qkj_YiQw1ZntDO3g')

# 페이지 로드를 기다림
time.sleep(5)

# BeautifulSoup을 사용하여 페이지의 HTML 분석
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 필요한 데이터 추출 (예: 앨범 목록)
albums = soup.find_all('발표곡')
for album in albums:
    print(album.text)

# 웹드라이버 종료
driver.quit()
