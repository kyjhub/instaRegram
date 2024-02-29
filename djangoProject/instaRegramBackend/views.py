from datetime import datetime

import geocoder as geocoder
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time
import urllib.request  # 이미지 저장 라이브러리
from PIL import  Image, ImageDraw, ImageFont

def temp_here(request):
    location = geocoder.ip('me').latlng
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    template=loader.get_template('index.html')
    context = {'temp': temp}
    return HttpResponse(template.render(context, request))

def instaCrawling(request):
    # url
    url=request.GET.get('url')
    print('HTML에서 넘어온 url: ',url)

    # 크롬 드라이버 생성
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/accounts/login/")
    driver.implicitly_wait(3)

    # 아이디
    id = request.GET.get('id')
    # 비밀번호
    pw = request.GET.get('password')

    # id와 pw를 입력하는 창의 요소 정보 획득
    input = driver.find_elements(By.TAG_NAME, 'input')
    print(input)
    # 아이디,비밀번호를 입력
    input[0].send_keys(id)
    input[1].send_keys(pw)
    # 로그인 버튼 엔터
    driver.find_elements(By.TAG_NAME, 'button')[0].click()
    driver.implicitly_wait(3)
    print('login success')

    # url = 'https://www.instagram.com/p/C1toc7up1EC/?utm_source=ig_web_copy_link'
    # 리그램하고싶은 url로 접속
    driver.get(url)
    driver.implicitly_wait(3)

    try:
        # 비디오 없다면 에러 발생
        # 영상 다운 // 영상은 1개라서 개수를 셀 필요는 없을듯
        videoSrc = driver.find_element(By.TAG_NAME, 'video').get_attribute('src')
        driver.implicitly_wait(5)  # 찾을 때 까지 대기
        urllib.request.urlretrieve(videoSrc, f'동영상.mp4')
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
            # 이미지 다운
            urllib.request.urlretrieve(imgSrc, f'이미지{i}.jpg')
            driver.implicitly_wait(5)  # 찾을 때 까지 대기
            image=Image.open(f'이미지{i}.jpg')
            width, height = image.size
            # 그림판에 이미지를 그대로 붙여넣는 느낌의 Draw() 함수
            draw = ImageDraw.Draw(image)
            #삽입할 워터마크 문자
            text = "samsungKorea"
            #삽입할 문자의 폰트 설정

            # step6.삽입할 문자의 높이, 너비 정보 가져오기
            width_txt, height_txt = draw.textsize(text)
            # step7.워터마크 위치 설정
            margin = 10
            x = width - width_txt - margin
            y = height - height_txt - margin
            # step8.텍스트 적용하기
            draw.text((x, y), text, fill='white')
            # step9.이미지 출력
            image.show()
            # step10.현재작업 경로에 완성 이미지 저장
            image.save("C:\study\toyProjects\instaRegram\djangoProject\watermakr.jpg")

            print(f'image{i} download success')
            if i != imgNum:
                driver.find_element(By.XPATH, "//button[@aria-label='다음']").click()
                driver.implicitly_wait(5)  # 찾을 때 까지 대기
    finally:
        # 게시글 글 클립보드에 복사
        text = driver.find_element(By.XPATH, "//div[@class='_a9zs']").text
        driver.implicitly_wait(5)  # 찾을 때 까지 대기
        addText = "#리그램 - @samsungkorea by @i___sang_\n"
        text = addText + text
        # 클립보드에 복사
        pyperclip.copy(text)

    time.sleep(10)
    print('end')
    return render(request,'success.html')