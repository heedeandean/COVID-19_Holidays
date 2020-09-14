import requests
from bs4 import BeautifulSoup as bs

import pandas as pd

import numpy as np
from datetime import datetime as dt

import matplotlib.pyplot as plt

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

soup = bs(html, 'html.parser')

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
        print('AttributeError :: date -> ', statedt.text)

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


# all_df.to_csv('nation_API_cnt_{}.csv'.format(dt.now().strftime('%Y_%m_%d')))


# 여기서 저는 확실한 데이터 프레임을 위해 NaN 값이 없는 부분 즉, 3월 2일의 데이터 부터 가져와서 시각화를 진행하겠습니다.
see_df = all_df[all_df['statedt'] >= '2020-03-02']

see_df.plot(x = 'statedt' , y = ['decidecnt','clearcnt'])
# plt.scatter(all_df['statedt'], all_df['deathcnt'])
# plt.scatter(all_df['statedt'], all_df['clearcnt'])
# plt.scatter(all_df['statedt'], all_df['accexamcnt'])
# plt.scatter(all_df['statedt'], all_df['carecnt'])
# plt.scatter(all_df['statedt'], all_df['resutlnegcnt'])

plt.title('Increase COVID19 in KOREA')
plt.xlabel('Date')

plt.show()


