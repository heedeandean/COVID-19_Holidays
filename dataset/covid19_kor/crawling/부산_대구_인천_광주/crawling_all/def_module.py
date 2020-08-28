from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd
import datetime as dt
from datetime import datetime
import requests
import json
import csv

class busan:
    def __init__(self):
        self.html_bs = None
        self.soup_bs = None
        self.ul_bs = None
        self.list_data_bs = []
        self.arr_data_bs = None
        self.bs_df = None

    def parser(self, url):
        self.html_bs = urlopen(url)
        self.soup_bs = BeautifulSoup(self.html_bs, "html.parser")
        self.ul_bs = self.soup_bs.select('#contents > div > div.corona_list > div.list_body > ul:nth-child(n)')

        for ul in self.ul_bs:
            num = ul.select('li:nth-of-type(1)')[0].text  # 확진번호
            route = ul.select('li:nth-of-type(4)')[0].text  # 감염경로 (접촉자, 교회 등)
            contact = ul.select('li:nth-of-type(6)')[0].text  # 접촉자 수
            isolation = ul.select('li:nth-of-type(4)')[0].text  # 격리장소
            cfmDate = ul.select('li:nth-of-type(2)')[0].text  # 확진일

            data_bs = (num, route, contact, isolation, cfmDate)
            self.list_data_bs.append(data_bs)

    def change_dataFrame(self):
        self.arr_data_bs = np.array(self.list_data_bs).reshape(-1, 5)
        col_name = ['area','cfmDate','route','contractCnt','gender','age']
        self.bs_df = pd.DataFrame(self.arr_data_bs[1:, (0, 4, 1, 2)], columns=col_name[:4])
        self.bs_df.insert(4, col_name[4], '-')  # 성별 없음
        self.bs_df.insert(5, col_name[5], '-')  # 나이 없음

    def bs_df_regex(self):

        # 0. 확진일자가 없는 경우 - 로 채우기
        for i in self.bs_df.index:
            if self.bs_df.loc[i, 'cfmDate'] == '':
                self.bs_df.loc[i, 'cfmDate'] = '-'

        # 1. xx..-  :: 표현식이 아닌 경우 삭제
        p = re.compile(r'[\D+]-')
        for i in self.bs_df.index:
            if p.search(self.bs_df.loc[i, 'area']) == None:
                self.bs_df = self.bs_df.drop(index=i)

        # 2. -00..  :: 표현식 삭제
        p = re.compile(r'-[\d+]')
        for i in self.bs_df.index:
            self.bs_df.loc[i, 'area'] = p.sub('', self.bs_df.loc[i, 'area'])

        # 3. 숫자 표현식 삭제
        p = re.compile(r'\d+')
        for i in self.bs_df.index:
            self.bs_df.loc[i, 'area'] = p.sub('', self.bs_df.loc[i, 'area'])

        # 4. (xxx...) :: (강서구 등) 표현식 삭제
        p = re.compile(r'[(]\D+[)]')
        for i in self.bs_df.index:
            self.bs_df.loc[i, 'area'] = p.sub('', self.bs_df.loc[i, 'area'])

        # 5. 띄어쓰기 삭제
        p = re.compile(r'\s+')
        for i in self.bs_df.index:
            self.bs_df.loc[i, 'area'] = p.sub('', self.bs_df.loc[i, 'area'])

        # 6. 타지역 발생자 삭제  / 삭제 사유 : 타지역 발생자 데이터는 제공하지 않음
        p = re.compile(r'부산')
        for i in self.bs_df.index:
            if p.search(self.bs_df.loc[i, 'area']) == None:
                self.bs_df = self.bs_df.drop(index=i)

        # 7. 날짜 표현 변경
        p1 = re.compile(r'\d+')
        for i in self.bs_df.index:
            try:
                month, day = p1.findall(self.bs_df.loc[i, 'cfmDate'])
                year = str(dt.datetime.now().year)
                hypn = '-'
                cfmdate = year + hypn + month + hypn + day
            except ValueError:
                cfmdate = self.bs_df.loc[i, 'cfmDate']
            self.bs_df.loc[i, 'cfmDate'] = cfmdate

        # 8. 확진자 수 ',' 없애주기 -> 나중에 int 형으로 바꾸기 쉽게
        p = re.compile(r'[,]')
        for i in self.bs_df.index:
            self.bs_df.loc[i, 'contractCnt'] = p.sub('', self.bs_df.loc[i, 'contractCnt'])

        return self.bs_df


class inchon:
    def __init__(self):
        self.html_ic = None
        self.soup_ic = None
        self.a_find_ic = None
        self.list_data_ic = []
        self.arr_data_ic = None
        self.ic_df = None

    def parser(self,url):
        self.html_ic = urlopen(url)
        self.soup_ic = BeautifulSoup(self.html_ic,"html.parser")
        self.a_find_ic = self.soup_ic.find_all('a', class_='patinet-profile')

        for a in self.a_find_ic:
            for strong in a:
                if strong.name == 'strong':
                    self.list_data_ic.append(strong.text)

                else:
                    self.list_data_ic.append(strong)

    def list_data_regex(self):
        # 부연설명 :: 인천은 html 형식 그대로 리스트를 긁어올 수 밖에 없어서 미리 배열로 만든 후
                    # 필요없는 열을 제거 후 다시 리스트로 풀어서 전처리 실행

        # 인천 컬럼 :: 확진일 / 감염경로

        # 리스트 형 -> 배열 형 변환 및 불필요 열 제거
        arr_data = np.array(self.list_data_ic).reshape(-1, 7)
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
        self.arr_data_ic = np.hstack((arr_data[:, :-1], pre_arr_data))

    def change_dataFrame(self):
        col_name = ['area', 'cfmDate', 'route', 'contractCnt', 'gender', 'age']
        self.ic_df = pd.DataFrame(self.arr_data_ic[:, (1, 2, 3)], columns=col_name[:-3])
        self.ic_df.insert(3, col_name[3], '-')  # 접촉자 수 없음
        self.ic_df.insert(4, col_name[4], '-')  # 성별 없음
        self.ic_df.insert(5, col_name[5], '-')  # 나이 없음
        self.ic_df['area'] = '인천'  # ~구 -> 인천으로 변경

    def ic_df_regex(self):
        # 1. 날짜 표현 변경
        p = re.compile(r'\d+')

        for i in self.ic_df.index:
            year, month, day = p.findall(self.ic_df.loc[i, 'cfmDate'])
            date = dt.datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d')
            self.ic_df.loc[i, 'cfmDate'] = date

        # 2. 감염경로 빈 값 '-' 로 채우기
        for i in self.ic_df.index:
            if self.ic_df.loc[i, 'route'] == '':
                self.ic_df.loc[i, 'route'] = '-'

        return self.ic_df


class gwangju:
    def __init__(self):
        self.list_gju = []
        self.gju_df = None


    def format_date(self,cfmDate):

        if (cfmDate != '-'):
            cfmDate = re.findall("\d+", cfmDate)

            if (len(cfmDate) == 2):
                cfmDate.insert(0, "2020")

            cfmDate = "-".join(cfmDate)
            cfmDate = datetime.strptime(cfmDate, "%Y-%m-%d").strftime("%Y-%m-%d")

        return cfmDate

    def format_detail_area(self, detail_area):
        detail_area = re.sub(r'[\s+]','',detail_area)
        if re.findall(r'[/]', detail_area) == ['/', '/']:
            gender, age, detail_area = re.split(r'[/]', detail_area)
            age = re.sub(r'[\D+]','',age) + 's'

            if gender == '남':
                gender = 'm'

            else:
                gender = 'f'

        else:
            gender, age, detail_area = ('-', '-', '-')

        return gender, age, detail_area

    def fill_list(self,empty_list):

        if not empty_list:
            result = '-'

        else:
            if (empty_list[0].text == ''):
                result = '-'
            else:
                result = empty_list[0].text

        return result

    def parser(self, url, html):
        url_gju = url
        html_gju = urlopen(html)

        # Json + parser
        req_gju = requests.get(url_gju)
        data_gju = json.loads(req_gju.text)

        # parser
        soup_gju = BeautifulSoup(html_gju, "html.parser")
        tag_gju = soup_gju.find_all("tr", {'class': "line_bg"})

        for line in data_gju["list"]:
            area = "광주"
            cfmDate = self.format_date(line["CONF_DATE"])
            route = line["INFECTION_PROCESS"]
            contactCnt = '-'

            # 새로 생긴 정보
            gender, age, detail_area = self.format_detail_area(line["PERSONAL_DATA"])

            data = (area, cfmDate, route, contactCnt, gender, age)

            self.list_gju.append(data)


        for td in tag_gju:
            area = "광주"
            cfmDate = self.format_date(td.select('td:nth-child(5)')[0].text)
            route = self.fill_list(td.select('td:nth-child(4)'))
            gender, age, detail_area = ('-', '-', '-')

            data = (area, cfmDate, route, contactCnt, gender, age)
            self.list_gju.append(data)

    def create_csv(self,list_area, area):

        today = datetime.now().strftime('%Y%m%d')
        file_name = area + '_' + today + '.csv'

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(list_area)

            print(file_name, "OK")

    def change_dataFrame(self):
        arr_data_gju = np.array(self.list_gju).reshape(-1, 6)
        col_name = ['area','cfmDate','route','contractCnt','gender','age']
        self.gju_df = pd.DataFrame(arr_data_gju[1:, :], columns=col_name)

        return self.gju_df


if __name__ == "__main__":

    # 부산시
    url = "http://www.busan.go.kr/covid19/Corona19/travelhist.do"
    busan = busan()
    busan.parser(url)
    busan.change_dataFrame()
    bs_df = busan.bs_df_regex()

    # 인천시
    url = 'https://www.incheon.go.kr/health/HE020409'
    inchon = inchon()
    inchon.parser(url)
    inchon.list_data_regex()
    inchon.change_dataFrame()
    ic_df = inchon.ic_df_regex()

    # 광주시
    url = "https://www.gwangju.go.kr/confiremListHome.do"
    html = "https://www.gwangju.go.kr/c19/c19/contentsView.do?pageId=coronagj2"
    gwangju = gwangju()
    gwangju.parser(url,html)
    gju_df= gwangju.change_dataFrame()


    # SAVE POINT
    frames = [bs_df, ic_df, gju_df]
    all_df = pd.concat(frames)
    all_df.to_csv('new_df_data_all_20200829.csv', encoding='UTF-8')





    # 중간에 뻑났을 때 확인하는 용도
    # np.savetxt('busan_arr/arr_data_bs_20200829_test.csv', busan.arr_data_bs, fmt='%s', delimiter=",", encoding='UTF-8')
    # np.savetxt('inchon_arr/arr_data_ic_20200829_test.csv', inchon.arr_data_ic, fmt='%s', delimiter=",", encoding='UTF-8')