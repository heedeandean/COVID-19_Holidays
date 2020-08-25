import requests
import json
import re
from datetime import datetime
import csv   
from urllib.request import urlopen
from bs4 import BeautifulSoup

url_gju = "https://www.gwangju.go.kr/confiremListHome.do" 
html_gju = urlopen("https://www.gwangju.go.kr/c19/c19/contentsView.do?pageId=coronagj2")   # 광주

req_gju = requests.get(url_gju)
data_gju = json.loads(req_gju.text)

soup_gju = BeautifulSoup(html_gju, "html.parser")
tag_gju = soup_gju.find_all("tr", {'class' : "line_bg"})


list_gju = []


def format_date(cfmDate):

    if (cfmDate != '-'):
        cfmDate = re.findall("\d+", cfmDate)

        if (len(cfmDate) == 2):
            cfmDate.insert(0, "2020")
        
        cfmDate = "-".join(cfmDate)
        cfmDate = datetime.strptime(cfmDate, "%Y-%m-%d").strftime("%Y-%m-%d")

    return cfmDate


def fill_list(empty_list):

    if not empty_list:
        result = '-'

    else:
        if (empty_list[0].text == ''):
            result = '-'
        else:
            result = empty_list[0].text 
    
    return result



for line in data_gju["list"]:

    area = "광주"
    cfmDate = format_date(line["CONF_DATE"])
    route = line["INFECTION_PROCESS"]
    contactCnt = '-'

    data = (area, cfmDate, route, contactCnt)
    list_gju.append(data)


for td in tag_gju:

    area = "광주"
    cfmDate = format_date(td.select('td:nth-child(5)')[0].text)
    route = fill_list(td.select('td:nth-child(4)'))
    contactCnt = '-' 

    data = (area, cfmDate, route, contactCnt)
    list_gju.append(data)



def create_csv(list_area, area):
    
    today = datetime.now().strftime('%Y%m%d')
    file_name = area + '_' + today + '.csv'

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_area)

        print(file_name, "OK")

create_csv(list_gju, "gju")