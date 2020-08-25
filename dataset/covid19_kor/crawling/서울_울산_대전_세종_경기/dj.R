# 대전 데이터
# url 불러오기
url <- 'https://www.daejeon.go.kr/corona19/index.do?menuId=0002'
html <- read_html(url, encoding = 'UFT-8')

df <- html %>% 
  html_nodes('.corona > tbody> tr> td') %>% 
  html_text() %>% 
  matrix()

df # 확인

# 데이터 전처리
dj_df <- str_trim(df, side="both")
dj_df <- matrix(dj_df, ncol=7, byrow = T)
dj_df <- data.frame(dj_df)
dj_df$X1 <- as.numeric(dj_df$X1)
dj_df <- dj_df %>% arrange(X1)
#View(dj_df) # 확인


# 대구지역만 추출
a <- c("동구","중구","서구","대덕","유성")
dj_table <- filter(dj_df, grepl(paste(a,collapse = "|"),X5))
#View(dj_table)

# 필요 데이터만 추출 
dj <- dj_table[,c(1,3,6)]
names(dj) <- c("area","cfmDate","route")
dj$contactCnt <- "-"
dj$area <- "대전"
dj$route[dj$route==""] <- "-" 
View(dj)


# 날짜
dj$cfmDate <- gsub("[[:punct:]]","",dj$cfmDate)

for (i in 1:length(dj$cfmDate)){
  if(nchar(dj$cfmDate[i])==2){
    dj$cfmDate[i] <- paste0(substr(dj$cfmDate[i], 1,1),"0",substr(dj$cfmDate[i],2,2))
  }
}

dj$cfmDate <- paste0("20200",dj$cfmDate)
dj$cfmDate <- as.Date(dj$cfmDate, "%Y%m%d")

View(dj)
write.csv(dj, 'C:/Users/user/Desktop/cov/dj200825.csv',row.names = F)
