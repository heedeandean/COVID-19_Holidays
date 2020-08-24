## 대전 ################################################## 
url <- 'https://www.daejeon.go.kr/corona19/index.do?menuId=0002'

Sys.setlocale("LC_ALL","English") 
# 오류를 피하기 위해 시스텀언어를 임시적으로 영어로 변경

html <- read_html(url, encoding = 'UTF-8')

df <- html %>% 
  html_table(fill = T) %>% 
  .[[1]]
Sys.setlocale("LC_ALL","Korean")

dj_table <- df %>% arrange(대전)
View(dj_table)
write.csv(dj_table, 'c:/workspaces/R/COVID_19/csv/dj_0824.csv',row.names = F)



## 세종 ###################################################

base_url <- 'https://www.sejong.go.kr/bbs/R3391/list.do?pageIndex='

urls <- NULL
for(x in 1:10){
  urls <- c(urls,paste(base_url,x, sep=''))
}
urls # 확인

sj <- NULL
for (url in urls){
  html <- read_html(url)
  sj <-c(sj, html %>% 
           html_nodes('a.item.onClk') %>% 
           html_text())
}

sj # 확인 

# 데이터 전처리
sj_df <- str_replace_all(sj,'\t',"")
sj_df <- str_trim(sj_df, side = 'both')
sj_df <- strsplit(sj_df, "\n|\n\n") 
sj_df # 확인


# 컬럼
num <- length(sj_df):1
no <- sapply(sj_df, "[",2)
area <-  sapply(sj_df, "[",3)
route <-  sapply(sj_df, "[",4)
date <-  sapply(sj_df, "[",5)
contact_num <- sapply(sj_df, '[',6)


# 테이블 생성
sj_table <- data.frame(num,no,area,route,date,contact_num)
sj_table <- sj_table %>% arrange(num)
View(sj_table) # 확인
write.csv(sj_table, 'c:/workspaces/R/COVID_19/csv/sj_0823.csv', row.names = F)



## 울산 ###################################################################
# url 불러오기
url <- 'http://www.ulsan.go.kr/corona.jsp'
html <- read_html(url, encoding = 'UFT-8')

df <- html %>% 
  html_nodes('#patient4') %>% 
  html_text()

# 데이터 전처리
us_df <- str_replace_all(df,"\r","")
us_df <- str_replace_all(us_df,'\t',"")
us_df <- strsplit(us_df, "\n|\n\n") 
us_df # 데이터 확인용


# 컬럼명 : "환자번호","거주지","추정 감염경로","확진일"
num <- length(us_df):1
no <- sapply(us_df, "[",1)
area <-  sapply(us_df, "[",2)
route <-  sapply(us_df, "[",3)
date <-  sapply(us_df, "[",4)

# 테이블 생성
us_table <- data.frame(num,no,area,route,date)
us_table <- us_table %>% arrange(num)
View(us_table) # 확인
write.csv(us_table, 'c:/workspaces/R/COVID_19/csv/us_0823.csv',row.names = F)


########################################################














