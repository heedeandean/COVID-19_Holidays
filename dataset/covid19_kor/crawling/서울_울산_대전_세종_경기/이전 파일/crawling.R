## 대전 ################################################## 
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


## 세종 #####################################################################
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
sj_table <- sj_table %>% arrange(num)
#View(sj_table) # 확인

# 필요한 데이터만 추출
sj <- sj_table[,c(2,5,4,6)]
names(sj) <- c("area","cfmDate","route","contactCnt")
sj$area <- "세종"


# 날짜
sj$cfmDate <- paste0("2020년",sj$cfmDate)
sj$cfmDate <- gsub("년|월|일","-",sj$cfmDate)
sj$cfmDate <- as.Date(sj$cfmDate)

View(sj)


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

## 서울 #####################################################################
# 데이터 가져오기
se_table <- read.csv("c:/workspaces/R/COVID_19/csv/seoul.csv")
#View(se_table)

# 필요한 데이터만 가져오기
se <- se_table %>% select("연번","확진일","접촉력")
names(se) <- c("area","cfmDate","route")
se <- se %>% arrange(area)
se$area <- "서울"
se$contactCnt <- "-"

# 날짜
se$cfmDate <- paste0("2020.",se$cfmDate)
se$cfmDate <- gsub("[[:punct:]]","-",se$cfmDate)
se$cfmDate <- as.Date(se$cfmDate)

View(se)

#############################################################################
# 데이터 합치기
all <- rbind(se,dj,us,sj)
View(all)
write.csv(all, 'C:/Users/user/Desktop/cov/all.csv',row.names = F)











