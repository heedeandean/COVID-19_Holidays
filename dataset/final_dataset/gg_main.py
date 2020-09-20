import pymysql  
import gg_utils as gu


# DB INSERT!
sql_exam = "insert ignore into Exam(exam_date, exam_cnt) values(%s,%s)"

sql_gginfo = "insert ignore into GGInfo(gginfo_id, loc, how_inf, relation) values(%s,%s,%s,%s)"
sql_gginfo_select = "select max(gginfo_id) from GGInfo"

sql_gginfo_csv = "insert into GGInfo(gginfo_id, gender, age, age_group, cfm_date, symptom_date, issymtom, route) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE gender=values(gender), age=values(age), age_group=values(age_group), cfm_date=values(cfm_date), symptom_date=values(symptom_date), issymtom=values(issymtom), route=values(route)"


conn = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='covid19', 
    charset='utf8'
)

with conn.cursor() as cur:


    # exam_list = gu.get_exam()    
    # cur.executemany(sql_exam, exam_list)
    # print("[Exam] 반영된 수 ", cur.rowcount)
    # print(len(exam_list))


    # cur.execute(sql_gginfo_select)
    # pastCnt = cur.fetchall()[0][0]

    # gg_list = gu.get_ggInfo(pastCnt)

    # if not gg_list:
    #     print("GGInfo테이블에 INSERT 할 것이 없습니다.")
    # else:
    #     cur.executemany(sql_gginfo, gg_list)
    #     print("[GGInfo] 반영된 수 ", cur.rowcount)
    #     print(len(gg_list))    


    gg_list_csv = gu.get_csvDown()    
    cur.executemany(sql_gginfo_csv, gg_list_csv)
    print("[GGInfo] 반영된 수 ", cur.rowcount)
    print(len(gg_list_csv))

