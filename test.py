from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Selenium 설정
chrome_options = Options()
# 필요한 경우 Chrome을 headless 모드로 실행하기 위한 옵션을 추가
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# 웹 페이지 로딩
driver.get('https://www.youtube.com/@LESSERAFIM_official/releases')

# 충분한 로딩 시간 대기
time.sleep(5)

# 페이지의 HTML 소스 가져오기
page_source = driver.page_source

# BeautifulSoup 객체 생성
soup = BeautifulSoup(page_source, 'html.parser')

# 'style-scope ytd-playlist-thumbnail' 클래스를 포함하는 모든 요소 찾기
elements = soup.find_all(class_='style-scope ytd-rich-grid-media')

# 중복 링크를 방지하기 위한 집합
found_hrefs = set()

# 링크 추출
for element in elements:
    # 각 요소의 부모에서 <a> 태그를 찾습니다.
    a_tag = element.find_parent('a')
    if a_tag:
        href = a_tag.get('href')
        if href and href not in found_hrefs:
            found_hrefs.add('https://www.youtube.com/' + href)  # 새로운 링크를 집합에 추가
            print(f"Found href: {href}")

for href in found_hrefs:
    print(href)
# 드라이버 종료
driver.quit()
