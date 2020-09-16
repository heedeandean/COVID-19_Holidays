import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import numpy as np

#### 적용 함수
def page_count(num):
    # 드라이버 설정
    # Mac_pc
    # path = './chromedriver'

    #Win_pc
    path = './chromedriver.exe'

    driver = webdriver.Chrome(path)

    driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(num))

    # 홀딩
    time.sleep(0.5)

    #파서
    html_kk = driver.page_source
    soup_kk = BeautifulSoup(html_kk, 'html.parser')

    # 카운팅 요소
    count = int(re.sub(r'[,]', '', soup_kk.select('#totalArticle')[0].text))  # 확진 건수
    pageNum = int(math.ceil(count / 15))  # 확진 건수 당 15개 씩 페이지 출력
    print('page count :: {}'.format(pageNum))

    return pageNum, driver

def driver_chrom(i):

    # 맥 드라이버 전용 + 자신과 맞는 크롬을 이용해서 드라이버 다운로드 하면 사용 가능
    # 드라이버 설정
    # Mac_pc
    # path = './chromedriver'

    # Win_pc
    path = './chromedriver.exe'
    driver = webdriver.Chrome(path)

    # 드라이버로 페이지 정보 가져오기
    driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(i))
    print('loading for page={}'.format(i))

    # 페이지 html 정보 가져오기
    html_kk = driver.page_source
    time.sleep(1)

    # 파서
    soup_kk = BeautifulSoup(html_kk, 'html.parser')
    tr_kk = soup_kk.select('#boardList > tbody > tr:nth-child(n)')

    return tr_kk

def attr_text(tr_kk):

    for tr in tr_kk:

        try:
            num = tr.select('td:nth-child(1)')[0].text  # 연번
            nation_num = tr.select('td:nth-child(2)')[0].text # 전국 번호
            cfmDate = tr.select('td:nth-child(3)')[0].text # 확진일
            loc = tr.select('td:nth-child(4)')[0].text # 지역
            how_inf = tr.select('td:nth-child(5)')[0].text # 발생 경위
            relation = tr.select('td:nth-child(6)')[0].text # 관련성
            isol = tr.select('td:nth-child(7)')[0].text # 격리병원
            data_kk = (num, nation_num, cfmDate, loc, how_inf, relation, isol)
        except IndexError:
            print('IndexError')
            driver.quit()
            tr_kk = driver_chrom(i)
            for tr in tr_kk:
                num = tr.select('td:nth-child(1)')[0].text  # 연번
                nation_num = tr.select('td:nth-child(2)')[0].text  # 전국 번호
                cfmDate = tr.select('td:nth-child(3)')[0].text  # 확진일
                loc = tr.select('td:nth-child(4)')[0].text  # 지역
                how_inf = tr.select('td:nth-child(5)')[0].text  # 발생 경위
                relation = tr.select('td:nth-child(6)')[0].text  # 관련성
                isol = tr.select('td:nth-child(7)')[0].text  # 격리병원
                data_kk = (num, nation_num, cfmDate, loc, how_inf, relation, isol)



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


# 리스트 -> 배열 변경
arr_data_kk = np.array(kk_list).reshape(-1,7)

# 세이브 포인트
np.savetxt('arr_data_kk_20200916.csv',arr_data_kk, fmt='%s', delimiter=",", encoding='UTF-8')

# 드라이브 종료
driver.quit()