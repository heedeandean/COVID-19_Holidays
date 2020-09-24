from selenium import webdriver
from time import sleep
from datetime import datetime
import csv
import os

# csv 다운로드
driver = webdriver.Chrome("./chromedriver.exe")
driver.implicitly_wait(10)

url = "https://public.tableau.com/views/2019nCoV_ver8_2_/19?%3Aembed=y&%3AshowVizHome=no&%3Ahost_url=https%3A%2F%2Fpublic.tableau.com%2F&%3Aembed_code_version=3&%3Atabs=yes&%3Atoolbar=yes&%3Aanimate_transition=yes&%3Adisplay_static_image=no&%3Adisplay_spinner=no&%3Adisplay_overlay=yes&%3Adisplay_count=yes&%3AloadOrderID=0"

driver.get(url)

sleep(3)
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[5]/span[1]').click()
sleep(3)
driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div/div[2]/div/button[3]').click()
sleep(3)
driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div/div[2]/div/div[2]/div[2]/div/label[2]').click()
sleep(3)
driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div/div[2]/div/div[3]/button').click()
sleep(10)


# 로컬 컴퓨터에 csv 다운로드 경로
path = 'C:/Users/user/Downloads/'

# csv 파일명 설정
today = datetime.now().strftime('%Y%m%d')
file_name = './gg_' + today + '.csv'

os.rename(path+'2.csv', path+file_name)


# csv 전처리
list_gg = []

with open(path+file_name,'r', encoding='utf-16') as f: 
    reader = csv.reader(f, delimiter = '\t') 
    next(reader)
    
    for row in reader:

        cfmDate = datetime.strptime(row[5], '%Y. %m. %d.').strftime('%Y-%m-%d')
        
        data = (row[0], cfmDate, row[6], row[7], row[11])
        list_gg.append(data)
        
print(list_gg)

