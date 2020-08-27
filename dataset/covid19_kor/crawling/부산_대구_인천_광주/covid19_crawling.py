from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import numpy as np
import re
import sys
import pandas as pd
import datetime as dt

# 콘솔 창에서 배열 다 확인 할 수 있도록 제공
np.set_printoptions(threshold=sys.maxsize)
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)




# html context 필요시
context = ssl._create_unverified_context()

# URL -> html 생성
html_bs = urlopen("http://www.busan.go.kr/covid19/Corona19/travelhist.do")
html_ic = urlopen('https://www.incheon.go.kr/health/HE020409')
# html_gj = urlopen('https://www.gwangju.go.kr/c19/c19/contentsView.do?pageId=coronagj2') <- 광주시 같은 경우 routeData 형식으로 되어있어 크롤링 불가
# 대구의 경우 기본 확진자 기본 컬럼만 제공

# parser 생성
soup_bs = BeautifulSoup(html_bs, "html.parser")
soup_ic = BeautifulSoup(html_ic,"html.parser")
#soup_gj = BeautifulSoup(html_gj, "html.parser")

# 속성 설정
ul_bs = soup_bs.select('#contents > div > div.corona_list > div.list_body > ul:nth-child(n)')
a_find_ic = soup_ic.find_all('a', class_ ='patinet-profile')
# tr_find_gj = soup_gj.find_all('tr', attrs={'class': "line_bg routeData"})


# 크롤링

## 리스트 초기화
list_data_bs = []
list_data_ic = []
# list_data_gj = []


## 부산시 parser

print('부산시 데이터 down_loading.... :: ')

for ul in ul_bs :

    num = ul.select('li:nth-of-type(1)')[0].text           # 확진번호
    route = ul.select('li:nth-of-type(4)')[0].text         # 감염경로 (접촉자, 교회 등)
    contact = ul.select('li:nth-of-type(6)')[0].text       # 접촉자 수
    isolation = ul.select('li:nth-of-type(4)')[0].text     # 격리장소
    cfmDate = ul.select('li:nth-of-type(2)')[0].text       # 확진일

    data_bs = (num,route,contact,isolation,cfmDate)
    list_data_bs.append(data_bs)

    # count load
    count_load = round(len(list_data_bs) / len(ul_bs) * 100,2)
    if len(list_data_bs) % 10 == 0:
        print(' 진행카운트 :: {} || 전체카운트 :: {} || 진행률 :: {} %'.format(len(list_data_bs),len(ul_bs),count_load))

    if count_load == 100.0 :
        print(' 진행카운트 :: {} || 전체카운트 :: {} || 진행률 :: {} %'.format(len(list_data_bs), len(ul_bs), count_load))

## 인천시 parser

print('인천시 데이터 down_loading.... :: ')

for a in a_find_ic:
    for strong in a :
        if strong.name == 'strong':
            list_data_ic.append(strong.text)

        else :
            list_data_ic.append(strong)

## 광주시 parser

# for tr in tr_find_gj :
#     print(tr)

## 정규표현식 변환
def re_inchon(list_data):

    # 리스트 형 -> 배열 형 변환 및 불필요 열 제거
    arr_data = np.array(list_data).reshape(-1, 7)
    arr_data = np.delete(arr_data, (0, 2, 5, 6), axis=1)

    # 전처리에 필요한 열 지정
    pre_arr_data = arr_data[:, 2]

    # 배열형 -> 문자열 형으로 변환 (re 패키지 적용)
    str_x = re.sub(r'[\r\n\t]', '', '+'.join(pre_arr_data))


    # (2020.xx.xx / 내용명 ) 형식으로 맞추기 위한 전처리 과정
    str_x = re.sub(r"\s+", '', str_x)
    str_x = re.sub(r"[(]\d\d[.]", '(2020.', str_x)
    str_x = re.sub('[(,)]', '', str_x)
    str_x = re.sub('[/]1인가구', '', str_x)
    str_x = re.sub('[/]재확진일', '', str_x)

    # 문자열 -> 리스트 형으로 변환
    pre_list_data = re.split('[+]|[/]', str_x)

    # 리스트 형 -> 배열형으로 변환
    pre_arr_data = np.array(pre_list_data).reshape(-1, 2)

    # 기본 배열 데이터 + 전처리 배열 데이터 조인
    join_arr_data = np.hstack((arr_data[:, :-1], pre_arr_data))

    return join_arr_data




## list -> matrix 형변환
arr_data_bs = np.array(list_data_bs).reshape(-1,5)
arr_data_ic = re_inchon(list_data_ic) # 전처리함수 내 배열형 자동 변환


# Save as csv = 매번 날짜 변경 (파일명 : 타입_데이터_지역_날짜)
np.savetxt('busan_arr/arr_data_bs_20200825.csv', arr_data_bs, fmt='%s', delimiter=",", encoding='UTF-8') # 부산시 데이터
np.savetxt('inchon_arr/arr_data_bs_20200825.csv', arr_data_ic, fmt='%s', delimiter=",", encoding='UTF-8') # 인천시 데이터



# 데이터 프레임으로 변환
col_name = ['area','cfmDate','route','contractCnt'] # 지역 / 확진일 / 감염경로 / 접촉자 수
col_name_plus = ['gender','age']

## 부산시
bs_df = pd.DataFrame(arr_data_bs[1:,(0,4,1,2)] , columns=col_name) # 0 : 지역 - 확진번호 / 4: 확진일 / 1: 감염 경로 / 2: 접촉자 수
bs_df.insert(4, col_name_plus[0], '-') # 성별 없음
bs_df.insert(5, col_name_plus[1], '-') # 나이 없음
## 인천시
ic_df = pd.DataFrame(arr_data_ic[:,(1,2,3)],columns=col_name[:-1])
ic_df.insert(3,col_name[3],'-') # 접촉자 수 없음
ic_df.insert(4, col_name_plus[0], '-') # 성별 없음
ic_df.insert(5, col_name_plus[1], '-') # 나이 없음
ic_df['area'] = '인천' # ~구 -> 인천으로 변경


# 데이터프레임 전처리

## 부산시

def bs_df_regex(bs_df):

    for i in bs_df.index:
        if bs_df.loc[i,'cfmDate'] == '':
            bs_df.loc[i,'cfmDate'] = '-'

    # 1. xx..-  :: 표현식이 아닌 경우 삭제
    p = re.compile(r'[\D+]-')
    for i in bs_df.index :
        if p.search(bs_df.loc[i,'area']) == None:
            bs_df = bs_df.drop(index=i)

    # 2. -00..  :: 표현식 삭제
    p = re.compile(r'-[\d+]')
    for i in bs_df.index :
        bs_df.loc[i,'area'] = p.sub('',bs_df.loc[i,'area'])

    # 3. 숫자 표현식 삭제
    p = re.compile(r'\d+')
    for i in bs_df.index :
        bs_df.loc[i, 'area'] = p.sub('',bs_df.loc[i, 'area'])


    # 4. (xxx...) :: (강서구 등) 표현식 삭제
    p = re.compile(r'[(]\D+[)]')
    for i in bs_df.index :
        bs_df.loc[i, 'area'] = p.sub('', bs_df.loc[i, 'area'])

    # 5. 띄어쓰기 삭제
    p = re.compile(r'\s+')
    for i in bs_df.index :
        bs_df.loc[i, 'area'] = p.sub('', bs_df.loc[i, 'area'])

    # 6. 타지역 발생자 삭제  / 삭제 사유 : 타지역 발생자 데이터는 제공하지 않음
    p = re.compile(r'부산')
    for i in bs_df.index :
        if p.search(bs_df.loc[i,'area']) == None:
            bs_df = bs_df.drop(index=i)

    # 7. 날짜 표현 변경
    p1 = re.compile(r'\d+')
    for i in bs_df.index:
        try:
            month, day = p1.findall(bs_df.loc[i, 'cfmDate'])
            year = str(dt.datetime.now().year)
            hypn = '-'
            cfmdate = year + hypn + month + hypn + day
        except ValueError:
            cfmdate = bs_df.loc[i, 'cfmDate']
        bs_df.loc[i, 'cfmDate'] = cfmdate

    # 8. 확진자 수 ',' 없애주기 -> 나중에 int 형으로 바꾸기 쉽게
    p = re.compile(r'[,]')
    for i in bs_df.index:
        bs_df.loc[i, 'contractCnt'] = p.sub('', bs_df.loc[i, 'contractCnt'])

    return bs_df

bs_df = bs_df_regex(bs_df)

## 인천시
def ic_df_regex(ic_df):
    # 1. 날짜 표현 변경
    p = re.compile(r'\d+')
    for i in ic_df.index :
        year, month, day = p.findall(ic_df.loc[i,'cfmDate'])
        date = dt.datetime(int(year),int(month),int(day)).strftime('%Y-%m-%d')
        ic_df.loc[i,'cfmDate'] = date

    # 2. 감염경로 빈 값 '-' 로 채우기
    for i in ic_df.index:
        if ic_df.loc[i, 'route'] == '':
            ic_df.loc[i, 'route'] = '-'

    return ic_df

ic_df = ic_df_regex(ic_df)




bs_df.to_csv('busan_df/df_data_bs_20200828.csv',encoding='UTF-8')
ic_df.to_csv('inchon_df/df_data_ic_20200828.csv',encoding='UTF-8')

frames = [bs_df,ic_df]

all_df = pd.concat(frames)

all_df.to_csv('df_data_all_20200828.csv',encoding='UTF-8')

