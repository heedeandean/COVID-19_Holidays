from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import numpy as np

# html context 필 시
context = ssl._create_unverified_context()

# URL -> html 생성
html_bs = urlopen("http://www.busan.go.kr/covid19/Corona19/travelhist.do")

# parser 생성
soup_bs = BeautifulSoup(html_bs, "html.parser")

# 속성 설정
div_bs = soup_bs.select('#contents > div > div.corona_list > div.list_body')

# 크롤링

for div in div_bs :
    #print(ul)
    for ul in div:

        for li in ul:
            print(li.find('li',{'class':'result'}))


'''
for ul in div_bs :

    for li in ul:
        # 기본 자료 (확진자 현황)
        num = li.select('li:nth-of-type(1)')[0].text # 확진번호
        route = li.select('li:nth-of-type(2)')[0].text # 감염경로 (접촉자, 교회 등)
        contact = li.select('li:nth-of-type(3)')[0].text # 접촉자 수
        isolation = li.select('li:nth-of-type(4)')[0].text # 격리장소
        cfmDate = li.select('li:nth-of-type(5)')[0].text # 확진일

        # 14일 뒤 삭제 자료 (확진자 이동경로)
        move_city1 = li.select('li.result > table > tbody > tr > td:nth-child(1)')[0].text부 # 시도
        move_city2 = li.select('li.result > table > tbody > tr > td:nth-child(2)')[0].text # 시군구
        move_category = li.select('li.result > table > tbody > tr > td:nth-child(3)')[0].text # 장소유형
        move_name = li.select('li.result > table > tbody > tr > td:nth-child(4)')[0].text # 상호명
        move_addr = li.select('li.result > table > tbody > tr > td:nth-child(5)')[0].text # 주소
        # move_time = li.select('li.result > table > tbody > tr > td:nth-child(6)')[0].text # 노출일시
        move_is_poe = li.select('li.result > table > tbody > tr > td:nth-child(7)')[0].text # 방역 여부

        print(move_city1)
'''