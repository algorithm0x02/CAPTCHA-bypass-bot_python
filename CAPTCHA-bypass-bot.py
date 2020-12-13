# -*- coding: utf-8 -*-
#version 1213

# 시스템 라이브러리 system libraries
import os
import random
import time

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

def delay ():
    time.sleep(random.randint(2,3))

try:
    #create chrome driver
    driver = webdriver.Chrome(os.getcwd()+"\\webdriver\\chromedriver.exe") 
    delay()
    #go to website
    driver.get("https://www.google.com/recaptcha/api2/demo")
    
except:
    print("")
    

#recaptcha 프레임으로 전환
frames=driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0]);
delay()

# 체크 박스를 클릭하여 recaptcha 활성화
driver.find_element_by_class_name("recaptcha-checkbox-border").click()


#recaptcha 오디오 제어 프레임으로 전환
driver.switch_to.default_content()
frames=driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

# audio challenge 클릭함
driver.find_element_by_id("recaptcha-audio-button").click()


#recaptcha 오디오 챌린지 프레임으로 전환
driver.switch_to.default_content()
frames= driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()


# 재생 버튼 클릭
driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
# mp3 오디오 파일 가져 오기
src = driver.find_element_by_id("audio-source").get_attribute("src")
print("[INFO] Audio src: %s"%src)


# 소스에서 mp3 오디오 파일 다운로드
urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav", format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
r= sr.Recognizer()

with sample_audio as source:
    audio = r.record(source)
    
#STT ( audio -> text) with google voice recognition 
key=r.recognize_google(audio)
print("Recaptcha Passcode: %s"%key)


#submit the results key!!!!
driver.find_element_by_id("audio-response").send_keys(key.lower())
driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
driver.switch_to.default_content()
delay()
driver.find_element_by_id("recaptcha-demo-submit").click()
delay()