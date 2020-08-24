library(tidyverse)
library(rvest)
library(dplyr)
library(XML)
library(stringr)
library(httr)

getwd()
setwd('/Users/jungunbae/workspaces/project/dataset/강원_충북_충남_전북')

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
chun3[,"접촉자수"] <- "확인불가"

chuncheon <- data.frame('시도'= chun3$'시도','지역'= chun3$'지역','확진일'= chun3$'확진일',
                        '인적사항'= chun3$'인적사항','추정감염경로'= chun3$'추정감염경로', '접촉자수'= chun3$'접촉자수' )



#원주시 
url2 <-  "https://www.wonju.go.kr/intro.jsp"
won <- url2 %>%
  read_html() %>%
  html_nodes('.titlebox>ul>li>p.text') %>%
  html_text() %>% data.frame()

won2 <- as.matrix(won)
won3 <- matrix(won2, ncol=5, byrow = T)
won3 <- as.data.frame(won3) 
names(won3) <- c('인적사항','추정감염경로','접촉자수', '격리시설', '확진일')
won3[,"시도"] <- "강원도"
won3[,"지역"] <- "원주시"
wonju <- data.frame('시도'= won3$'시도','지역'= won3$'지역','확진일'= won3$'확진일',
                    '인적사항'= won3$'인적사항','추정감염경로'= won3$'추정감염경로', '접촉자수'= won3$'접촉자수' )

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
gang3[,"추정감염경로"] <- "확인불가"
gang3[,"접촉자수"] <- "확인불가"

gangneung <- data.frame('시도'= gang3$'시도','지역'= gang3$'지역','확진일'= gang3$'확진일',
                        '인적사항'= gang3$'인적사항','추정감염경로'= gang3$'추정감염경로', '접촉자수'= gang3$'접촉자수' )


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

#속초시
#시도   지역   확진일   인적사항   추정감염경로   접촉자수
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
sok3[,"추정감염경로"] <- "확인불가"
sok3[,"접촉자수"] <- "확인불가"
sokcho <- data.frame('시도'= sok3$'시도','지역'= sok3$'지역','확진일'= sok3$'확진일',
                     '인적사항'= sok3$'인적사항','추정감염경로'= sok3$'추정감염경로', '접촉자수'= sok3$'접촉자수' )


#삼척시 -> 확진환자 0명(8.19 기준)
url7 <- "http://www.samcheok.go.kr/02179/02696.web"

#횡성군
url8 <- "https://www.hsg.go.kr/00001842/00002873.web"
hoeng <- url8 %>%
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
hoengsung <- data.frame('시도'= hoeng3$'시도','지역'= hoeng3$'지역','확진일'= hoeng3$'확진일',
                        '인적사항'= hoeng3$'인적사항','추정감염경로'= hoeng3$'추정감염경로', '접촉자수'= hoeng3$'접촉자수')



#영월군
url9 <- "https://www.yw.go.kr/www/selectBbsNttList.do?bbsNo=145&key=1240"


#평창군
url10 <- "https://www.pc.go.kr/corona-19.html"
pyeong <- url10 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()
pyeong2 <- as.matrix(pyeong)
pyeong3 <- matrix(pyeong2, ncol=5, byrow = T)
pyeong3 <- as.data.frame(pyeong3)
names(pyeong3) <- c('인적사항','증상발현','이동경로', '검사일자', '확진일')
pyeong3[,"시도"] <- "강원도"
pyeong3[,"지역"] <- "평창군"
pyeong3[,"추정감염경로"] <- "확인불가"
pyeong3[,"접촉자수"] <- "확인불가"
pyeongchang <- data.frame('시도'= pyeong3$'시도','지역'= pyeong3$'지역','확진일'= pyeong3$'확진일',
                          '인적사항'= pyeong3$'인적사항','추정감염경로'= pyeong3$'추정감염경로', '접촉자수'= pyeong3$'접촉자수' )

#철원군
url11 <- "https://www.cwg.go.kr/site/www/boardView.do?post=1632042&page=&boardSeq=319&key=3175"



#인제군
url12 <- "http://www.inje.go.kr/corona-19.html"
inje <- url12 %>%
  read_html() %>%
  html_nodes('.box>ul.conts>li>ul>li>p.text') %>%
  html_text() %>% data.frame()
inje2 <- as.matrix(inje)
inje3 <- matrix(inje2, ncol=5, byrow = T)
inje3 <- as.data.frame(inje3)
names(inje3) <- c('인적사항','이동경로', '확진일', '입원기관','상태')
inje3[,"시도"] <- "강원도"
inje3[,"지역"] <- "인제군"
inje3[,"추정감염경로"] <- "확인불가"
inje3[,"접촉자수"] <- "확인불가"
injegun <- data.frame('시도'= inje3$'시도','지역'= inje3$'지역','확진일'= inje3$'확진일',
                          '인적사항'= inje3$'인적사항','추정감염경로'= inje3$'추정감염경로', '접촉자수'= inje3$'접촉자수' )

#양양군 -> 확진자 0명(8.19 기준)
url13 <- "http://www.yangyang.go.kr/covid/corona-19.html"

gangwon <- rbind(chuncheon, wonju, gangneung,teabaek, sokcho,hoengsung,pyeongchang,injegun)
View(gangwon)
write.csv(gangwon, 'gangwon_2020_08_24.csv', row.names = F)


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

write.csv(chungbuk3, 'chungbuk_2020_08_24.csv', fileEncoding = 'utf8')

#####################################충남#########################################
url <- "http://www.chungnam.go.kr/coronaStatus.do?tab=2"
chung <- url %>%
  read_html() %>%
  html_nodes('div.tabContentInner>ul>li>table>tbody>tr>td') %>%
  html_text() %>% data.frame()
chung2 <- as.matrix(chung)
chung3 <- matrix(chung2, ncol=6, byrow = T)
chung3 <- as.data.frame(chung3)
names(chung3) <- c('환자','인적사항', '확진일','접촉자수', '격리시설', '이동경로')
chung3$이동경로 <- gsub('\n','', chung3$이동경로)
chung3$이동경로 <- gsub('\t','', chung3$이동경로)
chung3$이동경로 <- gsub('-','', chung3$이동경로)

nam <- chung3[grep("관련", chungnam3$이동경로),]
nam <- nam[,-c(2:5)]
names(nam) <- c('환자','추정감염경로')
chungnam <- merge(chung3,nam, by="환자", all = T)
write.csv(chungnam3, 'chungnam_2020_08_24.csv', row.names = T, fileEncoding = "utf8")
