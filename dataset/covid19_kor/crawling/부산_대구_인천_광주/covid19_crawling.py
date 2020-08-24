from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import numpy as np
import re
import sys
import numpy

# 콘솔 창에서 배열 다 확인 할 수 있도록 제공
numpy.set_printoptions(threshold=sys.maxsize)




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
list_data_gj = []


## 부산시 parser

print('부산시 데이터 down_loading.... :: ')

for ul in ul_bs :

    num = ul.select('li:nth-of-type(1)')[0].text           # 확진번호
    route = ul.select('li:nth-of-type(2)')[0].text         # 감염경로 (접촉자, 교회 등)
    contact = ul.select('li:nth-of-type(3)')[0].text       # 접촉자 수
    isolation = ul.select('li:nth-of-type(4)')[0].text     # 격리장소
    cfmDate = ul.select('li:nth-of-type(5)')[0].text       # 확진일

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




# Save as csv = 매번 날짜 변경 (덮어쓰기하면 예전꺼 날라가서 방법 몰라서 수작업으로 함 .. )
np.savetxt('bs_data_20200824.csv', arr_data_bs, fmt='%s', delimiter=",", encoding='UTF-8') # 부산시 데이터
np.savetxt('ic_data_20200824.csv', arr_data_ic, fmt='%s', delimiter=",", encoding='UTF-8') # 인천시 데이터









#############################    부산시 14일 동안 제공되는 이동경로 (이용X)      #############################


'''
list_move_bs = []


# table 속성 함수화
def arr_mapping_func(tbl):
    if tbl != []:
        y = []
        for cnt in range(len(tbl)):

            y.append(tbl[cnt].text)

        return y
    else:
        return ','







    tbl1 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(1)')
    tbl2 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(2)')
    tbl3 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(3)')
    tbl4 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(4)')
    tbl5 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(5)')
    # tbl6 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(6)')
    tbl7 = ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(7)')




    move_city1 =    arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(1)'))              # 시도
    move_city2 =    arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(2)'))              # 시군구
    move_category = arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(3)'))              # 장소유형
    move_name =     arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(4)'))              # 상호명
    move_addr =     arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(5)'))              # 주소
    # move_time =   arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(6)'))              # 노출일시
    move_is_poe =   arr_mapping_func(ul.select('li:nth-of-type(6) > table > tbody > tr > td:nth-child(7)'))              # 방역 여부

    move_bs = (move_city1,move_city2,move_category,move_name,move_addr,move_is_poe)
    list_move_bs.append(move_bs)

    # print(arr_mapping_func(tbl1),arr_mapping_func(tbl2),arr_mapping_func(tbl3),arr_mapping_func(tbl4),arr_mapping_func(tbl5),arr_mapping_func(tbl7))


arr_move_bs = np.array(list_move_bs).reshape(-1,6)

print(len(arr_move_bs))


#np.savetxt('bs_20200819_move.csv', arr_move_bs, fmt='%s', delimiter=",", encoding='UTF-8')
'''
