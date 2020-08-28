# 세종
base_url <- 'https://www.sejong.go.kr/bbs/R3391/list.do?pageIndex='

urls <- NULL
for(x in 1:10){
  urls <- c(urls,paste(base_url,x, sep=''))
}
#urls # 확인

sj <- NULL
for (url in urls){
  html <- read_html(url)
  sj <-c(sj, html %>% 
            html_nodes('a.item.onClk') %>% 
            html_text())
}


# 데이터 전처리
sj_df <- str_replace_all(sj,'\t',"")
sj_df <- str_trim(sj_df, side = 'both')
sj_df <- strsplit(sj_df, "\n|\n\n") 
#sj_df # 확인


# 컬럼
num <- length(sj_df):1
no <- sapply(sj_df, "[",2)
area <-  sapply(sj_df, "[",3)
route <-  sapply(sj_df, "[",4)
date <-  sapply(sj_df, "[",5)
contact_num <- sapply(sj_df, '[',6)


# 테이블 생성
sj_table <- data.frame(num,no,area,route,date,contact_num)
#View(sj_table) # 확인

# 필요한 데이터만 추출
sj <- sj_table[,c(2,5,4,6)]
names(sj) <- c("area","cfmDate","route","contactCnt")
sj$area <- "세종"


# 날짜
sj$cfmDate <- paste0("2020년",sj$cfmDate)
sj$cfmDate <- gsub("년|월|일","-",sj$cfmDate)
sj$cfmDate <- as.Date(sj$cfmDate)


# 성별, 나이대추가
sj$gender <- "-"
sj$age <- "-"

sj <- sj %>% arrange(cfmDate)

View(sj)
write.csv(sj, 'C:/Users/user/Desktop/cov/sj_200828.csv', row.names = F)
