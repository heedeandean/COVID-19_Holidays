# 울산 데이터
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
#us_df # 데이터 확인용


# 컬럼명 : "환자번호","거주지","추정 감염경로","확진일"
num <- length(us_df):1
no <- sapply(us_df, "[",1)
area <-  sapply(us_df, "[",2)
route <-  sapply(us_df, "[",3)
date <-  sapply(us_df, "[",4)

# 테이블 생성
us_table <- data.frame(num,no,area,route,date)
us_table <- us_table %>% arrange(num)
#View(us_table) # 확인

# 필요한 데이터만 추출
us <- us_table[,c(2,5,4)]
names(us) <- c("area","cfmDate","route")
us$area <- "울산"
us$contactCnt <- "-"

# 날짜
us$cfmDate <- paste0("2020/",us$cfmDate)
us$cfmDate <- as.Date(us$cfmDate)

View(us)
write.csv(us, 'C:/Users/user/Desktop/cov/us200825.csv',row.names = F)
