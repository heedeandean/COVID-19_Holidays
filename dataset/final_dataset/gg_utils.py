from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from datetime import datetime as dt
import os
import re
import math
import csv


# path = './chromedriver' # Mac_pc
path = './chromedriver.exe' # Win_pc

# 크롬 로컬 다운로드 경로(각 로컬 pc마다 상이함)
downPath = 'C:/Users/user/Downloads/'


########### 경기도 확진자 정보1 #####################

def get_ggInfo(pastCnt):

    #### 적용 함수
    def page_count(num):
        
        driver = webdriver.Chrome(path)
        driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(num))

        # 홀딩
        sleep(0.5)

        #파서
        html_kk = driver.page_source
        soup_kk = BeautifulSoup(html_kk, 'html.parser')

        # 카운팅 요소
        totalCnt = int(re.sub(r'[,]', '', soup_kk.select('#totalArticle')[0].text))  # 확진 건수
        crawCnt = totalCnt - pastCnt
        pageNum = int(math.ceil(crawCnt / 15))  # 확진 건수 당 15개 씩 페이지 출력
        print(">>>>>>>>>>>>", totalCnt, crawCnt, pageNum)
        print('page count :: {}'.format(pageNum))

        return pageNum, driver

    def driver_chrom(i):

        driver = webdriver.Chrome(path)

        # 드라이버로 페이지 정보 가져오기
        driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(i))
        print('loading for page={}'.format(i))

        # 페이지 html 정보 가져오기
        html_kk = driver.page_source
        sleep(1)

        # 파서
        soup_kk = BeautifulSoup(html_kk, 'html.parser')
        tr_kk = soup_kk.select('#boardList > tbody > tr:nth-child(n)')

        return tr_kk

    def attr_text(tr_kk):

        for tr in tr_kk:

            try:
                num = tr.select('td:nth-child(1)')[0].text  # 연번
                if (num == str(pastCnt)):
                    break
                # nation_num = tr.select('td:nth-child(2)')[0].text # 전국 번호
                # cfmDate = tr.select('td:nth-child(3)')[0].text # 확진일
                loc = tr.select('td:nth-child(4)')[0].text # 지역
                how_inf = tr.select('td:nth-child(5)')[0].text # 발생 경위
                relation = tr.select('td:nth-child(6)')[0].text # 관련성
                # isol = tr.select('td:nth-child(7)')[0].text # 격리병원
                # data_kk = (num, nation_num, cfmDate, loc, how_inf, relation, isol)
                data_kk = (num, loc, how_inf, relation)
            except IndexError:
                print('IndexError')
                driver.quit()
                tr_kk = driver_chrom(i)
                for tr in tr_kk:
                    num = tr.select('td:nth-child(1)')[0].text  # 연번
                    # nation_num = tr.select('td:nth-child(2)')[0].text  # 전국 번호
                    # cfmDate = tr.select('td:nth-child(3)')[0].text  # 확진일
                    loc = tr.select('td:nth-child(4)')[0].text  # 지역
                    how_inf = tr.select('td:nth-child(5)')[0].text  # 발생 경위
                    relation = tr.select('td:nth-child(6)')[0].text  # 관련성
                    # isol = tr.select('td:nth-child(7)')[0].text  # 격리병원
                    # data_kk = (num, nation_num, cfmDate, loc, how_inf, relation, isol)
                    data_kk = (num, loc, how_inf, relation)

            kk_list.append(data_kk)


    ########### 메인

    # 변수 초기화
    pageNum = 1
    kk_list = []
    html_page = None

    pageNum, driver = page_count(pageNum)


    # 1페이지 ~ pageNum 까지 크롤링
    for i in range(1,pageNum+1):
        tr_kk = driver_chrom(i)
        # 속성 뽑기
        attr_text(tr_kk)

        driver.quit()

    # 드라이브 종료
    driver.quit()

    return kk_list


# 파일 삭제 & return 파일 경로  
def rm_file(fileName):

    filePath = downPath + fileName

    if os.path.isfile(filePath):
        os.remove(filePath)

    return filePath


########### 경기도 확진자 정보2 #####################

def get_csvDown():
    
    filePath = rm_file('2.csv')

    # csv 다운로드
    driver = webdriver.Chrome(path)
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

    # csv 전처리
    list_gg = []

    with open(filePath,'r', encoding='utf-16') as f: 
        reader = csv.reader(f, delimiter = '\t') 
        next(reader)
        
        num = 0
        for row in reader:

            num += 1 # csv 연번이 일정하지 않았음
            cfmDate = dt.strptime(row[5], '%Y. %m. %d.').strftime('%Y-%m-%d')

            symptomDate = row[6]
            if (symptomDate != ''):
                symptomDate = dt.strptime(symptomDate, '%Y. %m. %d.').strftime('%Y-%m-%d')
        

            data = (num, row[2], row[3], row[4], cfmDate, symptomDate, row[7], row[11])
            list_gg.append(data)
            
    return list_gg



########### 검사자 추이 #####################

def get_exam():

    filePath = rm_file('검사자_추이_(전국)_(2)_data.csv')

    # csv 다운로드
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(10)

    url = "https://public.tableau.com/views/2019nCoV_ver8_2_/19_2?%3Aembed=y&%3AshowVizHome=no&%3Ahost_url=https%3A%2F%2Fpublic.tableau.com%2F&%3Aembed_code_version=3&%3Atabs=yes&%3Atoolbar=yes&%3Aanimate_transition=yes&%3Adisplay_static_image=no&%3Adisplay_spinner=no&%3Adisplay_overlay=yes&%3Adisplay_count=yes&%3AloadOrderID=0"

    driver.get(url)

    sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[36]/div/div/div/div/div[9]').click()
    sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[5]/span[1]').click()    
    sleep(3)
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div/div[2]/div/button[2]').click()    
    sleep(3)
    driver.switch_to.window(driver.window_handles[1]) # 팝업 창으로 전환
    sleep(3)
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/div[1]/div[2]/a').click()    
    sleep(10)

    # csv 전처리
    exam_list = []

    with open('C:/Users/user/Downloads/검사자_추이_(전국)_(2)_data.csv','r', encoding='utf-8') as f: 
        reader = csv.reader(f) 
        next(reader)
        
        for row in reader:
            cfmDate = dt.strptime(row[1], '%Y. %m. %d.').strftime('%Y-%m-%d')
            data = (cfmDate, row[2])
            exam_list.append(data)
            
    return exam_list

