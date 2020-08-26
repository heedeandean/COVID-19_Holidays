import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import numpy as np

#### 적용 함수
def attr_text(tr_kk,kk_list):

    for tr in tr_kk:
        num = tr.select('td:nth-child(1)')[0].text # 연번
        nation_num = tr.select('td:nth-child(2)')[0].text # 전국 번호
        cfmDate = tr.select('td:nth-child(3)')[0].text # 확진일
        loc = tr.select('td:nth-child(4)')[0].text # 지역
        how_inf = tr.select('td:nth-child(5)')[0].text # 발생 경위
        relation = tr.select('td:nth-child(6)')[0].text # 관련성
        isol = tr.select('td:nth-child(7)')[0].text # 격리병원
        data_kk = (num, nation_num, cfmDate, loc, how_inf, relation, isol)
        kk_list.append(data_kk)

    return kk_list



# 맥 드라이버 전용 + 자신과 맞는 크롬을 이용해서 드라이버 다운로드 하면 사용 가능
path = './chromedriver'
driver = webdriver.Chrome(path)

# 변수 초기화
pageNum = 1
kk_list = []
html_page = None

# 드라이버로 페이지 정보 가져오기
driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(pageNum))

# 드라이버 홀딩 시간
time.sleep(0.5)

# 페이지 html 정보 가져오기
html_kk = driver.page_source

# 파서
soup_kk = BeautifulSoup(html_kk, 'html.parser')

# 속성 설정
tr_kk = soup_kk.select('#boardList > tbody > tr:nth-child(n)')
kk_list = attr_text(tr_kk, kk_list)
count = int(re.sub(r'[,]','',soup_kk.select('#totalArticle')[0].text)) # 확진 건수

# 드라이버 종료
driver.quit()

# 테이블 페이지 지정
pageNum = int(math.ceil(count/15)) # 확진 건수 당 15개 씩 페이지 출력

# 2페이지 ~ pageNum 까지 크롤링
for i in range(2,pageNum+1):

    driver = webdriver.Chrome(path)

    driver.get('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page={}'.format(i))

    time.sleep(0.5)

    html_kk = driver.page_source

    tr_kk = soup_kk.select('#boardList > tbody > tr:nth-child(n)')
    kk_list = attr_text(tr_kk, kk_list)

    driver.quit()

arr_data_kk = np.array(kk_list).reshape(-1,7)

np.savetxt('arr_data_kk_20200826.csv',arr_data_kk, fmt='%s', delimiter=",", encoding='UTF-8')




















'''
costom_header = {
    'referer' : "https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903",
    # 'accept' : "application/json, text/javascript, */*; q=0.01",
    'user-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    # 'remote address' : '27.101.137.129:443'
}


html_url = urlopen('https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page=1')
url = 'https://www.gg.go.kr/ajax/board/getList.do'

req = requests.get(url, headers = costom_header)
print(req.text)
# data = json.load(req.text)
'''


