import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time
import urllib.request # 이미지 저장 라이브러리

#크롬 드라이버 생성
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")
driver.implicitly_wait(3)

#아이디
id='***'
#비밀번호
pw='***'

# id와 pw를 입력하는 창의 요소 정보 획득
input = driver.find_elements(By.TAG_NAME, 'input')
print(input)
# 아이디,비밀번호를 입력
input[0].send_keys(id)
input[1].send_keys(pw)
# 로그인 버튼 엔터
driver.find_elements(By.TAG_NAME,'button')[0].click()
driver.implicitly_wait(3)
print('login success')

url='https://www.instagram.com/p/C1toc7up1EC/?utm_source=ig_web_copy_link'
#리그램하고싶은 url로 접속
driver.get(url)
driver.implicitly_wait(3)

try:
    #비디오 없다면 에러 발생
    # 영상 다운 // 영상은 1개라서 개수를 셀 필요는 없을듯
    videoSrc=driver.find_element(By.TAG_NAME, 'video').get_attribute('src')
    driver.implicitly_wait(5)  # 찾을 때 까지 대기
    urllib.request.urlretrieve(videoSrc, f'동영상')
    driver.implicitly_wait(5)  # 찾을 때 까지 대기
except:
    print('there is no video')
    # 이미지 다운
    # 게시물 사진수
    imgIdxs = driver.find_elements(By.XPATH, "//div[@class='_acnb' or @class='_acnb _acnf']")
    imgNum = len(imgIdxs)
    # 각 이미지 다운
    for i in range(1, imgNum + 1):
        imgSrc = driver.find_element(By.XPATH, "//div[@class='_aagv']//img").get_attribute('src')
        driver.implicitly_wait(5)  # 찾을 때 까지 대기
        #urllib.request.urlretrieve(imgSrc, f'이미지{i}.jpg')
        driver.implicitly_wait(5)  # 찾을 때 까지 대기
        print(f'image{i} download success')
        if i != imgNum:
            driver.find_element(By.XPATH, "//button[@aria-label='다음']").click()
            driver.implicitly_wait(5)  # 찾을 때 까지 대기
finally:
    #게시글 글 클립보드에 복사
    text = driver.find_element(By.XPATH, "//div[@class='_a9zs']").text
    driver.implicitly_wait(5)  # 찾을 때 까지 대기
    addText="#리그램 - @samsungkorea by @i___sang_\n"
    text = addText+text
    #클립보드에 복사
    pyperclip.copy(text)

time.sleep(10)
print('end')