# 대전 데이터 
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
write.csv(dj_table, 'c:/workspaces/R/COVID_19/csv/dj_0819.csv',row.names = F)



