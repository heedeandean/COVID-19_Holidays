from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import numpy as np
import re
import requests
import json

context = ssl._create_unverified_context()

html_jn = urlopen("https://www.jeonnam.go.kr/coronaMainPage.do", context=context) # 전남
html_ph = urlopen("http://www.pohang.go.kr/COVID-19.html") # 경북(포항)
html_gj = urlopen("http://www.gyeongju.go.kr/area/page.do?mnu_uid=2860&") # 경북(경주)
html_gs = urlopen("http://gbgs.go.kr/programs/coronaMove/coronaMove.do") # 경북(경산)
html_uj = urlopen("http://www.uljin.go.kr/index.uljin?menuCd=DOM_000000110006003000") # 경북(울진)
html_gn = urlopen("http://xn--19-q81ii1knc140d892b.kr/main/main.do#close") # 경남

url_jj = "https://www.jeju.go.kr/api/article.jsp?board=corona_copper&pageSize=50" # 제주 (출처 : https://www.jeju.go.kr/corona19.jsp)


soup_jn = BeautifulSoup(html_jn.read(), "html.parser")
soup_ph = BeautifulSoup(html_ph, "html.parser")
soup_gj = BeautifulSoup(html_gj, "html.parser")
soup_gs = BeautifulSoup(html_gs, "html.parser")
soup_uj = BeautifulSoup(html_uj, "html.parser")
soup_gn = BeautifulSoup(html_gn, "html.parser")

req_jj = requests.get(url_jj)
data_jj = json.loads(req_jj.text)


tag_jn = soup_jn.select('body > div > div.covid-19-wrap > div.patients-way.patients-wayA > div.tbl-box.table_wrap_mobile.tblWrap > table > tbody')
tag_ph = soup_ph.find_all("div", {'class' : "item"})
tag_gj = soup_gj.find_all("ul", {'class' : "on"})
tag_gs = soup_gs.find_all("tbody")
tag_uj = soup_uj.find_all("tbody")
tag_gn = soup_gn.find_all("tr", {'id' : "patient4"})


list_jn = []
list_ph = []
list_gj = []
list_gs = []
list_uj = []
list_gn = []
list_jj = []


def fill_list(empty_list):
    
    if not empty_list:
        result = '-'
    else:
        result = empty_list[0].text 

    return result



for tr in tag_jn:

    for td in tr.select('tr:nth-of-type(odd)'):

        num = td.select('td:nth-of-type(1)')[0].text        # 확진자번호
        info = td.select('td:nth-of-type(2)')[0].text       # 인적사항
        route = td.select('td:nth-of-type(3)')[0].text      # 감염경로
        cfmDate = td.select('td:nth-of-type(4)')[0].text    # 확진일
        contact = td.select('td:nth-of-type(5)')[0].text    # 접촉
        isolation = td.select('td:nth-of-type(6)')[0].text  # 격리

        data = (num, info, route, cfmDate, contact, isolation)
        list_jn.append(data)


for div in tag_ph:

    num = div.select('p:nth-child(1) > span:nth-child(2)')[0].text       
    info = fill_list(div.select('p:nth-child(2) > span:nth-child(2)'))   
    route = fill_list(div.select('p:nth-child(6) > span:nth-child(2)'))  
    cfmDate = div.select('p:nth-child(4) > span:nth-child(2)')[0].text   
    isolation = div.select('p:nth-child(5) > span:nth-child(2)')[0].text 

    data = (num, info, route, cfmDate, isolation)
    list_ph.append(data)


for li in tag_gj:

    num = li.select('li:nth-of-type(1)')[0].text         
    route = li.select('li:nth-of-type(3)')[0].text      
    cfmDate = li.select('li:nth-of-type(4)')[0].text    
    isolation = li.select('li:nth-of-type(5)')[0].text  

    data = (num, route, cfmDate, isolation)
    list_gj.append(data)


for td in tag_gs:

    num = td.select('tr:nth-child(1) > td:nth-child(1)')[0].text            
    info = td.select('tr:nth-child(1) > td:nth-child(3)')[0].text           
    route = fill_list(td.select('tr:nth-child(1) > td:nth-child(6)'))       
    cfmDate = td.select('tr:nth-child(1) > td:nth-child(4)')[0].text        
    isolation = td.select('tr:nth-child(1) > td:nth-child(5)')[0].text      

    data = (num, info, route, cfmDate, isolation)
    list_gs.append(data)

del list_gs[0]


for td in tag_uj:
    num = td.select('tr:nth-child(1) > th')[0].text                    
    info = td.select('tr:nth-child(1) > td.point_bg')[0].text           
    route = td.select('tr:nth-child(1) > td:nth-child(3)')[0].text      
    cfmDate = td.select('tr:nth-child(1) > td:nth-child(4)')[0].text  
    isolation = td.select('tr:nth-child(1) > td:nth-child(6)')[0].text 

    data = (num, info, route, cfmDate, isolation)
    list_uj.append(data)


for td in tag_gn:

    num = td.select('td:nth-of-type(1)')[0].text.strip()
    info = td.select('td:nth-of-type(2)')[0].text.strip()
    route = td.select('td:nth-of-type(3)')[0].text.strip()
    cfmDate = td.select('td:nth-of-type(4)')[0].text.strip()
    isolation = re.sub(r"\W", "",  td.select('td:nth-of-type(5)')[0].text.strip())

    data = (num, info, route, cfmDate, isolation)
    list_gn.append(data)


for line in data_jj["articles"]:

    num = line["title"]
    info = line["add1"]
    route = line["add2"]
    cfmDate = line["add3"]
    contact = line["add4"]
    isolation = line["add5"]

    data = (num, info, route, cfmDate, contact, isolation)
    list_jj.append(data)

print("<<<<<<<<<<<<<<<<<<<<< 전      남 >>>>>>>>>>>>>>>>>>>>\n", list_jn, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경북(포항) >>>>>>>>>>>>>>>>>>>>\n", list_ph, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경북(경주) >>>>>>>>>>>>>>>>>>>>\n", list_gj, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경북(경산) >>>>>>>>>>>>>>>>>>>>\n", list_gs, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경북(울진) >>>>>>>>>>>>>>>>>>>>\n", list_uj, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 경      남 >>>>>>>>>>>>>>>>>>>>\n", list_gn, "\n")
print("<<<<<<<<<<<<<<<<<<<<< 제      주 >>>>>>>>>>>>>>>>>>>>\n", list_jj, "\n")




# csv
# arr_jn = np.array(list_jn).reshape(-1,6)
# arr_ph = np.array(list_ph).reshape(-1,5)


# np.savetxt('jn_20200819.csv', arr_jn, fmt='%s', delimiter=",", encoding='UTF-8')
# np.savetxt('ph_20200819.csv', arr_ph, fmt='%s', delimiter=",", encoding='UTF-8')
