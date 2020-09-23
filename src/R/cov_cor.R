# DB와 연결
#install.packages("RMySQL")
#install.packages("DBI")
library(RMySQL)
library(DBI)

drv = dbDriver("MySQL")
conn_covid = dbConnect(drv, host='127.0.0.1', port=3306, 
                       dbname='covid19', user='root', password='1234')

dbSendQuery(conn_covid, 'set character set utf8') 
dbListTables(conn_covid) 

# 국내 데이터 불러오기
query_g <- "select * from gginternal;"
cov_g <- dbGetQuery(conn_covid, query_g) 

# 일일 예상 감염률 : 유증상 * 3.5%(0.035) + 무증상 * 0.8%(0.008)  
gg <- cov_g
gg$spread <- (gg$symptom * 0.035)+(gg$asymptom * 0.008)
View(gg)


# 색상지정
col <- colorRampPalette(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA"))

# 선정한 변수3개와 확진자수의 상관관계 확인
#install.packages("corrplot")
library(corrplot)

# - 확진자와 정책
policy_cor <-  gg[,c(5,8)]
policy_cor <- cor(policy_cor)
corrplot(policy_cor,             # 상관행렬
         method = "ellipse",     # 모양으로 표현
         col = col(200),         # 색상 200개 선정
         type = "upper",         # 왼쪽 아래 행렬만 표시        
         addCoef.col = "black",  # 상관계수 색깔
         tl.col = "black",       # 변수명 색깔
         tl.srt = 0,             # 변수명 45도 기울임
         diag = FALSE)           # 대각 행렬 제외


# 확진자와 검사자수
exam_cor <-  gg[,c(5,7)]
exam_cor <- cor(exam_cor)
corrplot(exam_cor,               # 상관행렬
         method = "ellipse",     # 모양으로 표현
         col = col(200),         # 색상 200개 선정
         type = "upper",         # 왼쪽 아래 행렬만 표시        
         addCoef.col = "black",  # 상관계수 색깔
         tl.col = "black",       # 변수명 색깔
         tl.srt = 0,             # 변수명 45도 기울임
         diag = FALSE)           # 대각 행렬 제외


# 확진자와 2차 공격률
spread_cor <-  gg[,c(5,10)]
spread_cor <- cor(spread_cor)
corrplot(spread_cor,             # 상관행렬
         method = "ellipse",     # 모양으로 표현
         col = col(200),         # 색상 200개 선정
         type = "upper",         # 왼쪽 아래 행렬만 표시        
         addCoef.col = "black",  # 상관계수 색깔
         tl.col = "black",       # 변수명 색깔
         tl.srt = 0,             # 변수명 45도 기울임
         diag = FALSE)           # 대각 행렬 제외









