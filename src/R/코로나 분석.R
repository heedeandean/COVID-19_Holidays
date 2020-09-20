# DB와 연결
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

# 일일 예상 감염률 :  무증상 * 0.8%(0.008) + 유증상 * 3.5%(0.035)
gg <- cov_g
gg[is.na(gg)] <- 0
gg$risk <- (gg$symptom * 0.008)+(gg$asymptom * 0.035)
View(gg)

# 선정한 변수3개와 확진자수의 상관관계 확인
library(corrplot)
gg_df <- gg[,c(5,7,8,10)]
gg_cor <- cor(gg_df)

# 색상지정
col <- colorRampPalette(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA"))

# 상관행렬 히트맵 
corrplot(gg_cor,                   # 상관행렬
         method = "color",       # 색깔로 표현
         col = col(200),         # 색상 200개 선정
         type = "lower",         # 왼쪽 아래 행렬만 표시
         order = "hclust",       # 유사한 상관계수끼리 군집화
         addCoef.col = "black",  # 상관계수 색깔
         tl.col = "black",       # 변수명 색깔
         tl.srt = 45,            # 변수명 45도 기울임
         diag = FALSE)           # 대각 행렬 제외





