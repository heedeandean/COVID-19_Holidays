## 서울 ## 
url <- 'https://www.seoul.go.kr/coronaV/coronaStatus.do#route_page_top'

Sys.setlocale("LC_ALL","English") 
# 오류를 피하기 위해 시스텀언어를 임시적으로 영어로 변경

html <- read_html(url, encoding = 'UTF-8')

"""
# 테이블 위치 확인용
df1 <-  html %>% 
html_table(fill = T)
"""

df <- html %>% 
  html_table(fill = T) %>% 
  .[[7]]

Sys.setlocale("LC_ALL","Korean")

#df1 #위치 확인용

#View(df)

# 필요한 데이터만 추출
se <- df[,c(4,3,6)]
names(se) <- c("area","cfmDate","route")
se$area <- "서울"
se$contactCnt <- "-"

# 날짜
se$cfmDate <- paste0("2020.",se$cfmDate)
se$cfmDate <- gsub("[[:punct:]]","-",se$cfmDate)
se$cfmDate <- as.Date(se$cfmDate)

# 성별, 나이 추가
se$gender <- "-"
se$age <- "-"

se <- se %>% arrange(cfmDate)

View(se)
write.csv(se, 'C:/Users/user/Desktop/cov/se_200828.csv', row.names = F)

