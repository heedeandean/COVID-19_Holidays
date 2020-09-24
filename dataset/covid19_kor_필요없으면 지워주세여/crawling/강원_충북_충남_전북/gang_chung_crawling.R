library(tidyverse)
library(rvest)
library(dplyr)
library(XML)
library(stringr)
library(httr)
library(lubridate)

getwd()
setwd('/Users/jungunbae/workspaces/project/dataset/강원_충북_충남_전북')


"""
- area    # 지역        
 - cfmDate # 확진일(YYYY-MM-DD)
 - route   # 감염경로
 - contactCnt # 접촉자수(숫자)
 - gen # 성별(F/M)
 - age # 연령대(0s/10s/20s/.../80s/90s/100s)
 """
#################################강원도#######################################
#https://www.provin.gangwon.kr/covid-19.html
#시도   지역   확진일   인적사항   추정감염경로   접촉자수


#춘천시
url  <-"https://www.chuncheon.go.kr/index.chuncheon?menuCd=DOM_000000599001000000"

chun <- url %>%
  read_html() %>%
  html_nodes('.close>td') %>%
  html_text() %>% data.frame()
chun2 <- as.matrix(chun)
chun3 <- matrix(chun2, ncol=7, byrow = T)
chun3 <- as.data.frame(chun3) 
names(chun3) <- c('환자번호', '인적사항','감염지역','확진일','치료병원', '퇴원', '추정감염경로')


chun3[,"시도"] <- "강원도"
chun3[,"지역"] <- "춘천시"
chun3[,"접촉자수"] <- "-"
chun3[,"나이"] <- "-"
chun3[,"성별"] <- "-"


chuncheon <- data.frame('시도'= chun3$'시도','지역'= chun3$'지역','확진일'= chun3$'확진일',
                        '인적사항'= chun3$'인적사항','추정감염경로'= chun3$'추정감염경로', '접촉자수'= chun3$'접촉자수','나이'= chun3$'나이','성별'= chun3$'성별')

chuncheon$확진일 <- str_sub(chuncheon$확진일, 1, 8)
chuncheon$확진일 <- str_replace(chuncheon$확진일, '20.', '2020.')
chuncheon$확진일 <- gsub("[[:punct:]]","-",chuncheon$확진일)
chuncheon$확진일 <- as.Date(chuncheon$확진일)

#원주시 
url2 <-  "https://www.wonju.go.kr/intro.jsp"
won <- url2 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()
won2 <- as.matrix(won)
won3 <- matrix(won2, ncol=4, byrow = T)
won3 <- as.data.frame(won3) 
names(won3) <- c('인적사항','추정감염경로','확진일', '역학조사')
won3[,"시도"] <- "강원도"
won3[,"지역"] <- "원주시"
won3[,"접촉자수"] <- "-"

wonju <- data.frame('시도'= won3$'시도','지역'= won3$'지역','확진일'= won3$'확진일',
                    '인적사항'= won3$'인적사항','추정감염경로'= won3$'추정감염경로','접촉자수'= won3$'접촉자수')

wonju$확진일 <- paste0("2020/",wonju$확진일)
wonju$확진일 <- gsub("[[:punct:]]","-",wonju$확진일)
wonju$확진일 <- as.Date(wonju$확진일)
wonju <- wonju[!grepl("부천", wonju$인적사항),]
wonju <- wonju[!grepl("중랑", wonju$인적사항),]
wonju <- wonju[!grepl("서초", wonju$인적사항),]

wonju$나이 <- str_extract(wonju$인적사항, '10대|20대|30대|40대|50대|60대|70대|80대|90대') 
wonju$나이 <- gsub("대","s",wonju$나이)
wonju[,"성별"] <- "-"

#강릉시
url3 <-  "https://www.gn.go.kr/"
gang <- url3 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()

gang2 <- as.matrix(gang)
gang3 <- matrix(gang2, ncol=5, byrow = T)
gang3 <- as.data.frame(gang3) 
names(gang3) <- c('인적사항','이동경로','확진일', '격리시설', '퇴원')
gang3[,"시도"] <- "강원도"
gang3[,"지역"] <- "강릉시"
gang3[,"추정감염경로"] <- "-"
gang3[,"접촉자수"] <- "-"
gang3[,"나이"] <- "-"
gang3[,"성별"] <- "-"


gang3 <- gang3[grep("강릉", gang3$인적사항),]

gangneung <- data.frame('시도'= gang3$'시도','지역'= gang3$'지역','확진일'= gang3$'확진일',
                        '인적사항'= gang3$'인적사항','추정감염경로'= gang3$'추정감염경로', '접촉자수'= gang3$'접촉자수','나이'= gang3$'나이','성별'= gang3$'성별')

gangneung$확진일 <- ymd(gangneung$확진일)

#동해시 -> 확진환자 0명(8.19 기준)
url4 <- "https://www.dh.go.kr/corona19/01.htm"



#태백시
url5 <- "https://www.taebaek.go.kr/intro.jsp"
tae <- url5 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()

tae2 <- as.matrix(tae)
tae3 <- matrix(tae2, ncol=4, byrow = T)
tae3 <- as.data.frame(tae3) 
names(tae3) <- c('인적사항','추정감염경로','접촉자수', '격리시설')

tae3[,"시도"] <- "강원도"
tae3[,"지역"] <- "태백시"

baek <- url5 %>%
  read_html() %>%
  html_nodes('.sectionbox>table>tbody>tr>td') %>%
  html_text() %>% data.frame()
baek2 <- as.matrix(baek)
baek3 <- matrix(baek2, ncol=5, byrow = T)
baek3 <- as.data.frame(baek3) 
names(baek3) <- c('순번','확진일','인적사항', '격리시설', '퇴원')

teabaek <- data.frame('시도'= tae3$'시도','지역'= tae3$'지역','확진일'= baek3$'확진일',
                      '인적사항'= tae3$'인적사항','추정감염경로'= tae3$'추정감염경로', '접촉자수'= tae3$'접촉자수' )



teabaek$접촉자수 <- str_extract_all(teabaek$접촉자수, '[0-9]')

teabaek$나이 <- str_extract_all(teabaek$인적사항, '[0-9]{2}')
teabaek$나이[90 <=teabaek$나이 <=99] <- '90s' 
if(teabaek$나이 >= 100){ # 조건식1
  teabaek$나이 = "100s"
}else if(teabaek$나이 >= 90){ 
  teabaek$나이 = "90s"
}else if(teabaek$나이 >= 80){ 
  teabaek$나이 = "80s"
}else if(teabaek$나이 >= 70){ 
  teabaek$나이 = "70s"
}else if(teabaek$나이 >= 60){ 
  teabaek$나이 = "60s"
}else if(teabaek$나이 >= 50){ 
  teabaek$나이 = "50s"
}else if(teabaek$나이 >= 40){ 
  teabaek$나이 = "40s"
}else if(teabaek$나이 >= 30){ 
  teabaek$나이 = "30s"
}else if(teabaek$나이 >= 20){
  teabaek$나이 = "20s"
}else if(teabaek$나이 >= 10){ 
  teabaek$나이 = "10s"
}else{
  teabaek$나이 = "0s"
}

teabaek$성별 <- str_extract(teabaek$인적사항, '여|남') 
teabaek$성별 <- gsub("여","F",teabaek$성별)
teabaek$성별 <- gsub("남","M",teabaek$성별)

teabaek$확진일 <- gsub("월|화|수|목|금|토|일","",teabaek$확진일)
teabaek$확진일 <- ymd(teabaek$확진일)




#속초시
url6 <- "http://www.sokcho.go.kr/intro.html"
sok <- url6 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()

sok2 <- as.matrix(sok)
sok3 <- matrix(sok2, ncol=5, byrow = T)
sok3 <- as.data.frame(sok3) 
names(sok3) <- c('인적사항','이동경로','확진일', '격리시설', '퇴원')
sok3[,"시도"] <- "강원도"
sok3[,"지역"] <- "속초시"
sok3[,"추정감염경로"] <- "-"
sok3[,"접촉자수"] <- "-"
sok3[,"나이"] <- "-"
sok3[,"성별"] <- "-"

sokcho <- data.frame('시도'= sok3$'시도','지역'= sok3$'지역','확진일'= sok3$'확진일',
                     '인적사항'= sok3$'인적사항','추정감염경로'= sok3$'추정감염경로', '접촉자수'= sok3$'접촉자수','나이'= sok3$'나이','성별'= sok3$'성별' )
sokcho <- sokcho[grep("속초", sokcho$인적사항),]


#삼척시 -> 확진환자 0명(8.19 기준)
url7 <- "http://www.samcheok.go.kr/02179/02696.web"


#홍천군
url8 <- "https://www.hongcheon.go.kr/corona_intro.jsp"
hong <- url8 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()
hong2 <- as.matrix(hong)
hong3 <- matrix(hong2, ncol=5, byrow = T)
hong3 <- as.data.frame(hong3)
names(hong3) <- c('인적사항','이동경로','확진일', '추정감염경로', '격리시설')
hong3[,"시도"] <- "강원도"
hong3[,"지역"] <- "홍천군"
hong3[,"접촉자수"] <- "-"
hong3[,"나이"] <- "-"
hong3[,"성별"] <- "-"
hongcheon <- data.frame('시도'= hong3$'시도','지역'= hong3$'지역','확진일'= hong3$'확진일',
                        '인적사항'= hong3$'인적사항','추정감염경로'= hong3$'추정감염경로', '접촉자수'= hong3$'접촉자수','나이'= hong3$'나이','성별'= hong3$'성별')
hongcheon <- hongcheon[grep("홍천", hongcheon$인적사항),]

hongcheon$확진일 <- gsub("월|화|수|목|금|토|일","",hongcheon$확진일)
hongcheon$확진일 <- paste0("2020.",hongcheon$확진일)
hongcheon$확진일 <- ymd(hongcheon$확진일)



#횡성군
url9 <- "https://www.hsg.go.kr/00001842/00002873.web"
hoeng <- url9 %>%
  read_html() %>%
  html_nodes('div.info3 > div > span') %>%
  html_text() %>% data.frame()

hoeng2 <- as.matrix(hoeng)
hoeng3 <- matrix(hoeng2, ncol=5, byrow = T)
hoeng3 <- as.data.frame(hoeng3)
hoeng3 <- hoeng3[-1,]
names(hoeng3) <- c('인적사항','추정감염경로','접촉자수', '격리시설', '확진일')
hoeng3[,"시도"] <- "강원도"
hoeng3[,"지역"] <- "횡성군"
hoeng3[,"나이"] <- "-"
hoeng3[,"성별"] <- "-"

hoengsung <- data.frame('시도'= hoeng3$'시도','지역'= hoeng3$'지역','확진일'= hoeng3$'확진일',
                        '인적사항'= hoeng3$'인적사항','추정감염경로'= hoeng3$'추정감염경로', '접촉자수'= hoeng3$'접촉자수','나이'= hoeng3$'나이','성별'= hoeng3$'성별')

hoengsung <- hoengsung[grep("횡성", hoengsung$인적사항),]

hoengsung$확진일 <- gsub("월|화|수|목|금|토|일","",hoengsung$확진일)
hoengsung$확진일 <- paste0("2020.",hoengsung$확진일)
hoengsung$확진일 <- ymd(hoengsung$확진일)




#영월군
url10 <- "https://www.yw.go.kr/www/selectBbsNttList.do?bbsNo=145&key=1240"


#평창군
url11 <- "https://www.pc.go.kr/corona-19.html"
pyeong <- url11 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()
pyeong2 <- as.matrix(pyeong)
pyeong3 <- matrix(pyeong2, ncol=5, byrow = T)
pyeong3 <- as.data.frame(pyeong3)
names(pyeong3) <- c('인적사항','증상발현','이동경로', '검사일자', '확진일')
pyeong3[,"시도"] <- "강원도"
pyeong3[,"지역"] <- "평창군"
pyeong3[,"추정감염경로"] <- "-"
pyeong3[,"접촉자수"] <- "-"
pyeongchang <- data.frame('시도'= pyeong3$'시도','지역'= pyeong3$'지역','확진일'= pyeong3$'확진일',
                          '인적사항'= pyeong3$'인적사항','추정감염경로'= pyeong3$'추정감염경로', '접촉자수'= pyeong3$'접촉자수' )

pyeongchang <- pyeongchang[grep("평창", pyeongchang$인적사항),]

pyeongchang$확진일 <- gsub("월|화|수|목|금|토|일","",pyeongchang$확진일)
pyeongchang$확진일 <- ymd(pyeongchang$확진일)

pyeongchang$나이 <- str_extract(pyeongchang$인적사항, '10대|20대|30대|40대|50대|60대|70대|80대|90대') 
pyeongchang$나이 <- gsub("대","s",pyeongchang$나이)

pyeongchang$성별 <- str_extract(pyeongchang$인적사항, '여|남') 
pyeongchang$성별 <- gsub("여","F",pyeongchang$성별)
pyeongchang$성별 <- gsub("남","M",pyeongchang$성별)



#정선군
url12 <- "http://www.jeongseon.go.kr/intro.html"


#철원군
url13 <- "http://www.cwg.go.kr/coronaintro.jsp"

cheor <- url13 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()
cheor$.<- gsub("\r\n","",cheor$.)
cheor$.<- gsub("\t","",cheor$.)
cheor2 <- as.matrix(cheor)
cheor3 <- matrix(cheor2, ncol=4, byrow = T)
cheor3 <- as.data.frame(cheor3)
names(cheor3) <- c('인적사항','추정감염경로','치료시설', '확진일')
cheor3[,"시도"] <- "강원도"
cheor3[,"지역"] <- "철원군"
cheor3[,"접촉자수"] <- "-"
cheor3[,"나이"] <- "-"
cheor3[,"성별"] <- "-"


cheorwon <- data.frame('시도'= cheor3$'시도','지역'= cheor3$'지역','확진일'= cheor3$'확진일',
                          '인적사항'= cheor3$'인적사항','추정감염경로'= cheor3$'추정감염경로', '접촉자수'= cheor3$'접촉자수','나이'= cheor3$'나이', '성별'= cheor3$'성별')

cheorwon$확진일 <- paste0("20/",cheorwon$확진일)
cheorwon$확진일 <- ymd(cheorwon$확진일)
cheorwon <- cheorwon[!grepl("타지역",cheorwon$인적사항),]

#화천군
url14 <- "http://www.ihc.go.kr/corona.jsp"
hwa <- url14 %>%
  read_html() %>%
  html_nodes('.routebox>.itembox>ul>li>div>ul>li>p') %>%
  html_text() %>% data.frame()
hwa
hwa2 <- as.matrix(hwa)
hwa3 <- matrix(hwa2, ncol=6, byrow = T)
hwa3 <- as.data.frame(hwa3) 
names(hwa3) <- c('인적사항','감염지역','확진일','치료병원', '퇴원', '추정감염경로')
hwa3[,"시도"] <- "강원도"
hwa3[,"지역"] <- "화천군"
hwa3[,"접촉자수"] <- "-"
hwa3[,"나이"] <- "-"
hwa3[,"성별"] <- "-"

hwacheon <- data.frame('시도'= hwa3$'시도','지역'= hwa3$'지역','확진일'= hwa3$'확진일',
                       '인적사항'= hwa3$'인적사항','추정감염경로'= hwa3$'추정감염경로', '접촉자수'= hwa3$'접촉자수','나이'= hwa3$'나이', '성별'= hwa3$'성별')

hwacheon$확진일 <- ymd(hwacheon$확진일)

#양구군
url15 <- "http://www.inje.go.kr/corona-19.html"


#인제군
url16 <- "http://www.inje.go.kr/corona-19.html"
inje <- url16 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()
inje2 <- as.matrix(inje)
inje3 <- matrix(inje2, ncol=5, byrow = T)
inje3 <- as.data.frame(inje3)
names(inje3) <- c('인적사항','이동경로', '확진일', '입원기관','상태')
inje3[,"시도"] <- "강원도"
inje3[,"지역"] <- "인제군"
inje3[,"추정감염경로"] <- "-"
inje3[,"접촉자수"] <- "-"
injegun <- data.frame('시도'= inje3$'시도','지역'= inje3$'지역','확진일'= inje3$'확진일',
                          '인적사항'= inje3$'인적사항','추정감염경로'= inje3$'추정감염경로', '접촉자수'= inje3$'접촉자수' )


injegun$확진일 <- ymd(injegun$확진일)

injegun$나이 <- str_extract(injegun$인적사항, '10대|20대|30대|40대|50대|60대|70대|80대|90대') 
injegun$나이 <- gsub("대","s",injegun$나이)

injegun$성별 <- str_extract(injegun$인적사항, '여|남') 
injegun$성별 <- gsub("여","F",injegun$성별)
injegun$성별 <- gsub("남","M",injegun$성별)


#고성군 
url17 <- "https://www.gwgs.go.kr/"


#양양군 
url18 <- "http://www.yangyang.go.kr/covid/corona-19.html"
yang <- url18 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()
yang2 <- as.matrix(yang)
yang3 <- matrix(yang2, ncol=5, byrow = T)
yang3 <- as.data.frame(yang3)
names(yang3) <- c('인적사항','이동경로', '확진일', '입원기관','상태')
yang3[,"시도"] <- "강원도"
yang3[,"지역"] <- "양양군"
yang3[,"추정감염경로"] <- "-"
yang3[,"접촉자수"] <- "-"
yang3[,"나이"] <- "-"
yang3[,"성별"] <- "-"

yangyang <- data.frame('시도'= yang3$'시도','지역'= yang3$'지역','확진일'= yang3$'확진일',
                       '인적사항'= yang3$'인적사항','추정감염경로'= yang3$'추정감염경로', '접촉자수'= yang3$'접촉자수','나이'= yang3$'나이', '성별'= yang3$'성별')



yangyang$확진일 <- gsub("월|화|수|목|금|토|일","",yangyang$확진일)
yangyang$확진일 <- paste0("2020.",yangyang$확진일)
yangyang$확진일 <- ymd(yangyang$확진일)

yangyang <- yangyang[grep("양양", yangyang$인적사항),]

##############강원도 통합##################
gangwon <- rbind(chuncheon,wonju,gangneung,teabaek,hongcheon,hoengsung,pyeongchang,cheorwon,hwacheon,injegun,yangyang)
gangwon$접촉자수 <- as.character(gangwon$접촉자수)


gangwon_f <- data.frame(area= gangwon$시도,cfmDate= gangwon$확진일,route= gangwon$추정감염경로, contactCnt= gangwon$접촉자수,gender= gangwon$성별,age= gangwon$나이)

write.csv(gangwon_f, 'gangwon_200828.csv', row.names = F, fileEncoding = "utf8")




#######################################충북#######################################
url <- "http://www1.chungbuk.go.kr/covid-19/index.do"
chungbuk <- url %>%
  read_html() %>%
  html_nodes('.layer>table>tbody>tr>td') %>%
  html_text() %>% data.frame()

chungbuk2 <- chungbuk %>% group_by(.) %>% mutate(id = row_number())
chungbuk2 <- arrange(chungbuk2,desc(id))
chungbuk2 <- chungbuk2[-c(1:212),]
chungbuk2 <- chungbuk2[,-2]
chungbuk2 <- as.matrix(chungbuk2)
chungbuk3 <- matrix(chungbuk2, ncol=6, byrow = T)
chungbuk3 <- as.data.frame(chungbuk3)
chungbuk3<- chungbuk3[,c(6,5,4,3,2,1)]
names(chungbuk3) <- c('확진자','확진일', '나이','거주지', '감염경로', '조치사항')
chungbuk3[,"시도"] <- "충북"
chungbuk3[,"접촉자수"] <- "-"
chungbuk3[,"성별"] <- "-"

chungbuk4 <- chungbuk3[grep("충북", chungbuk3$확진자),]

chungbuk4$확진일 <- paste0("2020.",chungbuk4$확진일)
chungbuk4$확진일 <- ymd(chungbuk4$확진일)

chungbuk4$나이 <- gsub("대","s",chungbuk4$나이)
chungbuk4$나이 <- gsub("10s미만","0s",chungbuk4$나이)


chungbuk_f <- data.frame(area= chungbuk4$시도,cfmDate= chungbuk4$확진일,route= chungbuk4$감염경로, contactCnt= chungbuk4$접촉자수,gender= chungbuk4$성별,age= chungbuk4$나이)


write.csv(chungbuk_f, 'chungbuk_200828.csv', row.names = F, fileEncoding = "utf8")


View(chungbuk_f)
#####################################충남#########################################
url <- "http://www.chungnam.go.kr/coronaStatus.do?tab=2"
chungnam <- url %>%
  read_html() %>%
  html_nodes('div.tabContentInner>ul>li>table>tbody>tr>td') %>%
  html_text() %>% data.frame()
chungnam2 <- as.matrix(chungnam)
chungnam3 <- matrix(chungnam2, ncol=6, byrow = T)
chungnam3 <- as.data.frame(chungnam3)
names(chungnam3) <- c('환자','인적사항', '확진일','접촉자수', '격리시설', '이동경로')
chungnam3$이동경로 <- gsub('\n','', chungnam3$이동경로)
chungnam3$이동경로 <- gsub('\t','', chungnam3$이동경로)
chungnam3$이동경로 <- gsub('-','', chungnam3$이동경로)

chungnam3[,"시도"] <- "충남"
chungnam3[,"감염경로"] <- "-"
chungnam3[,"성별"] <- "-"

chungnam3$나이 <- str_extract(chungnam3$인적사항, '유아|아동|영아|10대|20대|30대|40대|50대|60대|70대|80대|90대') 
chungnam3$나이 <- gsub("대","s",chungnam3$나이)
chungnam3$나이 <- gsub("유아|아동|영아","0s",chungnam3$나이)

chungnam3$확진일 <- gsub("월",".",chungnam3$확진일)
chungnam3$확진일 <- gsub("일",".",chungnam3$확진일)
chungnam3$확진일 <- paste0("2020.",chungnam3$확진일)
chungnam3$확진일 <- ymd(chungnam3$확진일)

chungnam3$접촉자수 <- gsub("명","",chungnam3$접촉자수)

chungnam_f <- data.frame(area= chungnam3$시도,cfmDate= chungnam3$확진일,route= chungnam3$감염경로, contactCnt= chungnam3$접촉자수,gender= chungnam3$성별,age= chungnam3$나이)


View(chungnam_f)
write.csv(chungnam_f, 'chungnam_200828.csv', row.names = F, fileEncoding = "utf8")


################################통합####################

all <- rbind(gangwon_f, chungbuk_f, chungnam_f)
View(all)
write.csv(all, 'gangwon_chungbuk_chungnam_200828.csv', row.names = F, fileEncoding = "utf8")

