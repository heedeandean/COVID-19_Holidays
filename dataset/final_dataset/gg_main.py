import pymysql  

import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import pandas as pd
import numpy as np

from selenium import webdriver
from time import sleep
import os
import re
import math
import csv


# path = './chromedriver' # Mac_pc
path = './chromedriver.exe' # Win_pc


########### 경기도 확진자 정보 #####################

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



def get_csvDown():
    
    # 기존 csv 삭제
    filePath = 'C:/Users/user/Downloads/2.csv'

    if os.path.isfile(filePath):
        os.remove(filePath)

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




########### 전국 검사 현황 #####################
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

serviceKey = 'GsGMbaDETPd05r326o0ICejVO%2BU%2FXwTQES1Tf8Vl3wL0fuYEMxV%2F3Ai2pLmcPFT9yWXTlE9DwTf7H1dR3ezWgg%3D%3D'
pageNo = 1
numOfRows = 10
startCreateDt = '20200101'
endCreateDt = dt.now().strftime('%Y%m%d')

url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/\
getCovid19InfStateJson?\
serviceKey={}&pageNo={}&numOfRows={}&startCreateDt={}&endCreateDt={}&'

url = url.format(serviceKey, pageNo, numOfRows, startCreateDt, endCreateDt)

response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

item = soup.find_all('item')


# 제공해 주는 컬럼은 다음과 같습니다.
# 게시글 번호 / 기준일 / 기준시간 / 확진자 수 / 사망자 수 / 격리해제 수 / 검사진행 수
# 치료중 환자 수 / 결과 음성 수 / 누적 검사 수 / 누적 검사 완료 수 / 누적 확진률 / 등록 일시분초 / 수정 일시분초


# 현재 API 에서 제공해주는 순서 컬럼은 다음과 같습니다.
# col_name = ['accdefrate', 'accexamcnt', 'accexamcompcnt', 'carecnt', 'clearcnt', 'createdt', 'deathcnt',
#             'decidecnt', 'examcnt', 'resutlnegcnt', 'seq',  'statetime', 'updatedt']


# 이 중 기준시간, 등록 일시분초, 수정 일시분초 컬럼은 필요 없다 판단하여 컬럼에서 제거 하겠습니다.
# 만약 필요하시면 추가 하시면 되겠습니다.

col_name = ['seq','statedt','decidecnt', 'deathcnt','clearcnt','examcnt',
            'carecnt','resutlnegcnt','accexamcnt','accexamcompcnt','accdefrate']


# 데이터 프레임 형 변수 설정
all_df = pd.DataFrame(columns=col_name)

# 파서
for tag in item:
    try:
        accdefrate = tag.find('accdefrate') # 확진률 , float
        accexamcnt = tag.find('accexamcnt') # 누적 검사수 , int
        accexamcompcnt = tag.find('accexamcompcnt')# 누적 검사완료수 , int
        carecnt = tag.find('carecnt') # 치료중인 환자 수 , int
        clearcnt = tag.find('clearcnt') # 격리해제 수 , int
        # createdt = tag.find('createdt')
        deathcnt = tag.find('deathcnt') # 누적 사망자 수 , int
        decidecnt = tag.find('decidecnt') # 누적 확진자 수 , int
        examcnt = tag.find('examcnt') # 검사 수 , int
        resutlnegcnt = tag.find('resutlnegcnt') # 검사 음성 수 , int
        seq = tag.find('seq') # 고유값 , str
        statedt = tag.find('statedt') # 기준일 , date
        # statetime = tag.find('statetime')
        # updatedt = tag.find('updatedt')

        date = dt.strptime(statedt.text, '%Y%m%d')
        date = date.strftime('%Y-%m-%d')

        clean_list = [seq.text, date, decidecnt.text, deathcnt.text, clearcnt.text, examcnt.text,
                      carecnt.text, resutlnegcnt.text, accexamcnt.text, accexamcompcnt.text, accdefrate.text]
        # print(clean_list)
        all_df = all_df.append(pd.Series(clean_list, index=all_df.columns), ignore_index=True)

    except AttributeError:
        # 다음사항은 text 함수가 공백(None)으로 받아들여 예외사항으로 넘어온 구간입니다.
        # 2020-03-01 전 까지 제공하지 않은 컬럼, 컬럼 내 Null 값은 다음과 같습니다.
        # accdefrate = Null
        # carecnt , resutlnegcnt , accexamcnt, accexamcompcnt
        # 특이 사항은 statedt 값이 2개 있는거로 보아 하루에 2번 제공을 한 것 같습니다.

        # 따라서 처음에 리스트를 지정해준 곳에 수동으로 np.nan 값을 넣어줍니다.
        # print('AttributeError :: date -> ', statedt.text)

        date = dt.strptime(statedt.text, '%Y%m%d')
        date = date.strftime('%Y-%m-%d')
        clean_list = [seq.text, date, decidecnt.text, deathcnt.text, clearcnt.text, examcnt.text,
                      np.nan, np.nan, np.nan, np.nan, np.nan]
        # print(clean_list)

        all_df = all_df.append(pd.Series(clean_list, index=all_df.columns), ignore_index=True)


# 데이터 타입을 변경합니다.
all_df[['seq', 'decidecnt', 'deathcnt', 'clearcnt', 'examcnt','carecnt', 'resutlnegcnt', 'accexamcnt', 'accexamcompcnt','accdefrate']] = \
    all_df[['seq', 'decidecnt', 'deathcnt', 'clearcnt', 'examcnt','carecnt', 'resutlnegcnt', 'accexamcnt', 'accexamcompcnt','accdefrate']].apply(pd.to_numeric)

all_df['statedt'] = pd.to_datetime(all_df['statedt'])


# 중복 데이터 관련해서 전처리 해줍니다.
merge_1 = all_df.groupby(['statedt','examcnt'])['examcnt'].mean()
merge_1 = merge_1.groupby(['statedt']).sum()
merge_1 = pd.DataFrame(merge_1).reset_index(level=['statedt'])
merge_1 = merge_1.rename({'examcnt':'x_exam'}, axis= 'columns')

merge_2 = all_df.drop_duplicates(['statedt'],keep='first')

merge = pd.merge(merge_2,merge_1,on='statedt')

# examcnt 를 지우고 x_exam 을 추가하면서 컬럼을 다시 원래대로 돌려놓습니다.
all_df = merge[['seq','statedt','decidecnt', 'deathcnt','clearcnt','x_exam',
            'carecnt','resutlnegcnt','accexamcnt','accexamcompcnt','accdefrate']]

all_df = all_df.rename({'x_exam':'examcnt'}, axis= 'columns')

all_df = all_df.where((pd.notnull(all_df)), None)

# 리스트 변환
exam_list = all_df.values.tolist()

for i in range(len(exam_list)):
    exam_list[i][1] = exam_list[i][1].strftime('%Y-%m-%d')



# DB INSERT!
sql_exam = "insert ignore into Exam(exam_id, statedt, decidecnt, deathcnt, clearcnt, examcnt, carecnt, resutlnegcnt, accexamcnt, accexamcompcnt, accdefrate) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

sql_gginfo = "insert into GGInfo(gginfo_id, loc, how_inf, relation) values(%s,%s,%s,%s)"
sql_gginfo_select = "select max(gginfo_id) from GGInfo"

sql_gginfo_csv = "insert into GGInfo(gginfo_id, gender, age, age_group, cfm_date, symptom_date, issymtom, route) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE gender=values(gender), age=values(age), age_group=values(age_group), cfm_date=values(cfm_date), symptom_date=values(symptom_date), issymtom=values(issymtom), route=values(route)"


conn = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='covid19', 
    charset='utf8'
)

with conn:
    cur = conn.cursor()

    # cur.executemany(sql_exam, exam_list)
    # print("[Exam] 반영된 수 ", cur.rowcount)
    print(len(exam_list))


    # cur.execute(sql_gginfo_select)
    # pastCnt = cur.fetchall()[0][0]
    # gg_list = get_ggInfo(pastCnt)
    # if not gg_list:
    #     print("GGInfo테이블에 INSERT 할 것이 없습니다.")
    # else:
    #     cur.executemany(sql_gginfo, gg_list)
    #     print("[GGInfo] 반영된 수 ", cur.rowcount)
    #     print(len(gg_list))    


    # gg_list_csv = get_csvDown()    
    # print(gg_list_csv)
    # cur.executemany(sql_gginfo_csv, gg_list_csv)
    # print("[GGInfo] 반영된 수 ", cur.rowcount)
    # print(len(gg_list_csv))

