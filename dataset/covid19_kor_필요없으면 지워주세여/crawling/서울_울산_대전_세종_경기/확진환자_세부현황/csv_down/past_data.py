import csv
import pymysql  
from datetime import datetime as dt

list_gg = []

with open('C:/Users/user/Desktop/past_data/경기도 빅데이터 공모전 - 경기도 데이터.csv','r', encoding='utf-8') as f: 
    reader = csv.reader(f)
    next(reader)
    
    for row in reader:
        # cfmDate = dt.strptime(row[5], '%Y. %m. %d.').strftime('%Y-%m-%d')
        
        data = (row[0], row[17], row[18], row[19])
        list_gg.append(data)



# DB INSERT!
# sql_gginfo = "insert ignore into GGInfo(gginfo_id, loc, how_inf, relation) values(%s,%s,%s,%s)"

sql_gginfo = "insert into GGInfo(gginfo_id, loc, how_inf, relation) values(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE loc=values(loc), how_inf=values(how_inf), relation=values(relation)"

conn = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='covid19', 
    charset='utf8'
)

with conn:
    cur = conn.cursor()

    cur.executemany(sql_gginfo, list_gg)
    print("[GGInfo] 반영된 수 ", cur.rowcount)


print(len(list_gg))


##########################################
# list_gg = []

# filePath = 'C:/Users/user/Downloads/2.csv'

# with open(filePath,'r', encoding='utf-16') as f: 
#     reader = csv.reader(f, delimiter = '\t') 
#     next(reader)
    
#     for row in reader:

#         cfmDate = dt.strptime(row[5], '%Y. %m. %d.').strftime('%Y-%m-%d')

#         symptomDate = row[6]
#         if (symptomDate != ''):
#             symptomDate = dt.strptime(symptomDate, '%Y. %m. %d.').strftime('%Y-%m-%d')


#         data = (row[0], row[2], row[3], row[4], cfmDate, symptomDate, row[7], row[11])
#         list_gg.append(data)
        

# print(list_gg)