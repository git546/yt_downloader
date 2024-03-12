from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

chrome_options = Options()
# 필요한 경우, Chrome을 headless 모드로 실행하기 위한 옵션을 추가
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# 유튜브 아티스트 채널로 이동
driver.get('https://www.youtube.com/@LESSERAFIM_official/releases')

# "발표곡" 섹션을 찾아 클릭 이벤트 시뮬레이션
time.sleep(5) # 페이지 로딩 대기
tab = driver.find_element(By.CSS_SELECTOR, '[tab-title="발표곡"]')
tab.click()

# 클릭 후 콘텐츠 로딩을 위해 충분한 시간 대기
time.sleep(5)

# 변경된 페이지 소스로 BeautifulSoup 객체 생성
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 변경된 페이지에서 원하는 정보 추출
# 예를 들어, 동적으로 로드된 비디오 제목들을 가져오기
# 정확한 선택자는 페이지 구조에 따라 다를 수 있으므로, 실제 페이지를 검사하여 확인 필요
videos = soup.find_all('a', class_='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media')
for video in videos:
    print(video.text.strip())

driver.quit()
