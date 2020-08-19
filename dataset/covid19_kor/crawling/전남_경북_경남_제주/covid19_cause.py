from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import numpy as np

context = ssl._create_unverified_context()

html_jn = urlopen("https://www.jeonnam.go.kr/coronaMainPage.do", context=context) # 전남
html_ph = urlopen("http://www.pohang.go.kr/COVID-19.html") # 경북(포항)


soup_jn = BeautifulSoup(html_jn.read(), "html.parser")
soup_ph = BeautifulSoup(html_ph, "html.parser")

trs_jn = soup_jn.select('body > div > div.covid-19-wrap > div.patients-way.patients-wayA > div.tbl-box.table_wrap_mobile.tblWrap > table > tbody')
divs_ph = soup_ph.find_all("div", {'class' : "item"})


list_jn = []
list_ph = []


def fill_list(empty_list):
    
    if not empty_list:
        result = '-'
    else:
        result = empty_list[0].text 

    return result



for tr in trs_jn:
    print(type(tr))

    for td in tr.select('tr:nth-of-type(odd)'):

        num = td.select('td:nth-of-type(1)')[0].text        # 확진자번호
        info = td.select('td:nth-of-type(2)')[0].text       # 인적사항
        route = td.select('td:nth-of-type(3)')[0].text      # 감염경로
        cfmDate = td.select('td:nth-of-type(4)')[0].text    # 확진일
        contact = td.select('td:nth-of-type(5)')[0].text    # 접촉
        isolation = td.select('td:nth-of-type(6)')[0].text  # 격리

        data_jn = (num, info, route, cfmDate, contact, isolation)
        list_jn.append(data_jn)




for div in divs_ph:

    num = div.select('p:nth-child(1) > span:nth-child(2)')[0].text       # 확진자번호
    info = fill_list(div.select('p:nth-child(2) > span:nth-child(2)'))   # 인적사항
    route = fill_list(div.select('p:nth-child(6) > span:nth-child(2)'))  # 감염경로
    cfmDate = div.select('p:nth-child(4) > span:nth-child(2)')[0].text   # 확진일
    isolation = div.select('p:nth-child(5) > span:nth-child(2)')[0].text # 격리

    data_ph = (num, info, route, cfmDate, isolation)
    list_ph.append(data_ph)


print("<<<<<<<<<<<<<<<<<<<<< 전남 >>>>>>>>>>>>>>>>>>>>\n", list_jn, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경북(포항) >>>>>>>>>>>>>>>>>>>>\n", list_ph, "\n")


# 매트릭스 변환 - 수정 :: 우현 20200819
arr_jn = np.array(list_jn).reshape(-1,6)
arr_ph = np.array(list_ph).reshape(-1,5)


'''
# Save csv - 수정 :: 우현 20200819
np.savetxt('jn_20200819.csv', arr_jn, fmt='%s', delimiter=",", encoding='UTF-8')
np.savetxt('ph_20200819.csv', arr_ph, fmt='%s', delimiter=",", encoding='UTF-8')
'''