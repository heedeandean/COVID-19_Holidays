from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import requests
import json
from datetime import datetime
import csv   

context = ssl._create_unverified_context()

html_jn = urlopen("https://www.jeonnam.go.kr/coronaMainPage.do", context=context)       # 전남
html_ph = urlopen("http://www.pohang.go.kr/COVID-19.html")                              # 경북(포항)
html_gj = urlopen("http://www.gyeongju.go.kr/area/page.do?mnu_uid=2860&")               # 경북(경주)
html_gs = urlopen("http://gbgs.go.kr/programs/coronaMove/coronaMove.do")                # 경북(경산)
html_uj = urlopen("http://www.uljin.go.kr/index.uljin?menuCd=DOM_000000110006003000")   # 경북(울진)
html_gn = urlopen("http://xn--19-q81ii1knc140d892b.kr/main/main.do#close")              # 경남

url_jj = "https://www.jeju.go.kr/api/article.jsp?board=corona_copper&pageSize=50"       # 제주 (출처 : https://www.jeju.go.kr/corona19.jsp)


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
tag_gs = soup_gs.find_all("table", {'class' : "table01"})
tag_uj = soup_uj.find_all("tbody")
tag_gn = soup_gn.find_all("tr", {'id' : "patient4"})


list_jn = []
list_ph = []
list_gj = []
list_gs = []
list_uj = []
list_gn = []
list_jj = []


def format_date(cfmDate):

    if (cfmDate != '-'):
        cfmDate = re.findall("\d+", cfmDate)

        if (len(cfmDate) == 2):
            cfmDate.insert(0, "2020")
        
        cfmDate = "-".join(cfmDate)
        cfmDate = datetime.strptime(cfmDate, "%Y-%m-%d").strftime("%Y-%m-%d")

    return cfmDate


def format_contactCnt(contactCnt):

    if (contactCnt == '-' or contactCnt == "조사중"):
        contactCnt = '-'

    elif (contactCnt == "없음" or contactCnt == None):
        contactCnt = 0

    else: 
        contactCnt = re.findall("\d+", contactCnt)[0]    

    return contactCnt


def fill_list(empty_list):

    if not empty_list:
        result = '-'

    else:
        if (empty_list[0].text == ''):
            result = '-'
        else:
            result = empty_list[0].text 
    
    return result



for tr in tag_jn:

    for td in tr.select('tr:nth-of-type(odd)'):

        area = "전남"                                                    # 지역
        cfmDate = format_date(td.select('td:nth-of-type(4)')[0].text)    # 확진일
        route = td.select('td:nth-of-type(3)')[0].text                   # 감염경로
        contactCnt = format_contactCnt(td.select('td:nth-of-type(5)')[0].text)              # 접촉자수

        data = (area, cfmDate, route, contactCnt)
        list_jn.append(data)



for div in tag_ph:

    area = "경북(포항)"
    cfmDate = format_date(div.select('p:nth-child(4) > span:nth-child(2)')[0].text)
    route = fill_list(div.select('p:nth-child(6) > span:nth-child(2)'))  
    contactCnt = '-'

    data = (area, cfmDate, route, contactCnt)
    list_ph.append(data)

    

for li in tag_gj:

    area = "경북(경주)"
    cfmDate = format_date(li.select('li:nth-of-type(4)')[0].text)    
    route = re.sub(r"\W", "-", li.select('li:nth-of-type(3)')[0].text)      
    contactCnt = '-'

    data = (area, cfmDate, route, contactCnt)
    list_gj.append(data)



for td in tag_gs:

    area = "경북(경산)"
    cfmDate = format_date(td.select('tbody > tr:nth-child(1) > td:nth-child(4)')[0].text)        
    obj = fill_list(td.select('tbody > tr:nth-child(1) > td:nth-child(6)')).split('(')[0].strip()       

    if (obj.isdigit()):
        route = '-'
        contactCnt = obj
    else:
        route = obj
        contactCnt = '-'

    data = (area, cfmDate, route, contactCnt)
    list_gs.append(data)



for td in tag_uj:

    area = "경북(울진)"
    cfmDate = format_date(td.select('tr:nth-child(1) > td:nth-child(4)')[0].text)  
    route = td.select('tr:nth-child(1) > td:nth-child(3)')[0].text  
    contactCnt = '-'    

    data = (area, cfmDate, route, contactCnt)
    list_uj.append(data)



for td in tag_gn:

    area = "경남"
    cfmDate = format_date(td.select('td:nth-of-type(4)')[0].text.split(',')[0])
    route = td.select('td:nth-of-type(3)')[0].text.strip()
    contactCnt = '-' 

    data = (area, cfmDate, route, contactCnt)
    list_gn.append(data)



for line in data_jj["articles"]:

    area = "제주"
    cfmDate = format_date(line["add3"])

    route = line["add2"]
    if(route == None): route = '-'
        
    contactCnt = format_contactCnt(line["add4"])

    data = (area, cfmDate, route, contactCnt)
    list_jj.append(data)



# print("<<<<<<<<<<<<<<<<<<<<< 전      남 >>>>>>>>>>>>>>>>>>>>\n", list_jn, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 경북(포항) >>>>>>>>>>>>>>>>>>>>\n", list_ph, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 경북(경주) >>>>>>>>>>>>>>>>>>>>\n", list_gj, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 경북(경산) >>>>>>>>>>>>>>>>>>>>\n", list_gs, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 경북(울진) >>>>>>>>>>>>>>>>>>>>\n", list_uj, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 경      남 >>>>>>>>>>>>>>>>>>>>\n", list_gn, "\n")
# print("<<<<<<<<<<<<<<<<<<<<< 제      주 >>>>>>>>>>>>>>>>>>>>\n", list_jj, "\n")


def create_csv(list_area, area):
    
    today = datetime.now().strftime('%Y%m%d')
    file_name = area + '_' + today + '.csv'

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_area)

        print(file_name, "OK")

create_csv(list_jn, "jn")
create_csv(list_ph, "ph")
create_csv(list_gj, "gj")
create_csv(list_gs, "gs")
create_csv(list_uj, "uj")
create_csv(list_gn, "gn")
create_csv(list_jj, "jj")

