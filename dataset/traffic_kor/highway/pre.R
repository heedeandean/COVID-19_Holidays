# http://data.ex.co.kr/portal/traffic/trafficRegion#
# 일자는 최대 30일간 뽑을 수 있음 
# X 축단위 - 일 / 자료종류 - 총합 / 권역 - 경기권역 / 비교대상 - 일 / 
# 수작업으로 csv 다운받아 기본 데이터는 trafic_20170101_20200731.csv 로 만들음

install.packages("ggplot2")
library(stringr)
library(ggplot2)
library(lattice)

# 전처리 패키지
install.packages("dplyr")
library(dplyr)

# 날짜 데이터로 형변환 하기 위한 패키지
install.packages('tidyverse') 
library('tidyverse')

install.packages('lubridate')
library('lubridate')


table <- read.csv('/Users/kim-uhyeon/Documents/corona/COVID-19_Holidays/dataset/covid19_Trafic_count/trafic_20170101_20200731.csv', na = "-", fileEncoding = "CP949", encoding = "UTF-8") # 초기화
View(table)

table$IO2[table$IO =='입구'] <- 'in'
table$IO2[table$IO =='출구'] <- 'out'
table$IO2[table$IO =='합계'] <- 'sum'



# 특수문자 ',' 제거 
table$trafic2 <- str_replace_all(table$trafic[],'[[:punct:]]','')

# 형변환 char -> num
table$trafic2 <- as.numeric(table$trafic2)

# 형변환 char -> date 
table$date2 <- ymd(table$date)

# 테이블 분리 (출입별)
table_in <- table %>% filter(IO2 == 'in') %>% select(date2,trafic2)
table_out <- table %>% filter(IO2 == 'out') %>% select(date2,trafic2)
table_sum <- table %>% filter(IO2 == 'sum') %>% select(date2,trafic2)

# 테이블 년도 및 월별 분류

## 출입량
table_in$year <- year(table_in$date2)
table_in$month <- month(table_in$date2)
table_in_2017_month <- table_in  %>% filter(year == 2017) %>% select(date2, trafic2,year,month) 
table_in_2018_month <- table_in  %>% filter(year == 2018) %>% select(date2, trafic2,year,month) 
table_in_2019_month <- table_in  %>% filter(year == 2019) %>% select(date2, trafic2,year,month) 

## 출구량
table_out$year <- year(table_out$date2)
table_out$month <- month(table_out$date2)
table_out_2017_month <- table_out  %>% filter(year == 2017) %>% select(date2, trafic2,year,month) 
table_out_2018_month <- table_out  %>% filter(year == 2018) %>% select(date2, trafic2,year,month) 
table_out_2019_month <- table_out  %>% filter(year == 2019) %>% select(date2, trafic2,year,month) 

## 합계량
table_sum$year <- year(table_sum$date2)
table_sum$month <- month(table_sum$date2)
table_sum_2017_month <- table_sum  %>% filter(year == 2017) %>% select(date2, trafic2,year,month) 
table_sum_2018_month <- table_sum  %>% filter(year == 2018) %>% select(date2, trafic2,year,month) 
table_sum_2019_month <- table_sum  %>% filter(year == 2019) %>% select(date2, trafic2,year,month) 

# 전체 합계 / 평균
## 합계량 3674860282     2809526
sum_trafic_summarise <- table %>%filter(IO2 == 'sum') %>% 
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))

## 출입량 1828385851     1397849
in_trafic_summarise <- table %>%filter(IO2 == 'in') %>% 
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))

##출구량 1846474431     1411678
out_trafic_summarise <- table %>%filter(IO2 == 'out') %>% 
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))

# 연도별 합계량 / 평균량

## 입구량 
in_trafic_year_summarise <- table_in %>% group_by(year) %>%
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))

## 출구량
out_trafic_year_summarise <- table_out %>% group_by(year) %>%
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))

## 합계량 
sum_trafic_year_summarise <- table_sum %>% group_by(year) %>%
  summarise(trafic_sum = sum(trafic2) , trafic_mean = as.integer(mean(trafic2)))


# 각연도별 월별 합계량 / 평균량

## 입구량 
in_trafic_2017_summarise <- table_in_2017_month %>%
  group_by(month) %>%
  summarise(trafic_sum = sum(trafic2), trafic_mean = as.integer(mean(trafic2)))

in_trafic_2018_summarise <- table_in_2018_month %>%
  group_by(month) %>%
  summarise(trafic_sum = sum(trafic2), trafic_mean = as.integer(mean(trafic2)))

in_trafic_2019_summarise <- table_in_2019_month %>%
  group_by(month) %>%
  summarise(trafic_sum = sum(trafic2), trafic_mean = as.integer(mean(trafic2)))

## 출구량 



# 2017 설날 교통량 데이터
table$trafic2[table$date=='20170127'] # [1] 1222272 1032825 2255097
table$trafic2[table$date=='20170128'] # [1] 1433756 1434264 2868020 설날 당일
table$trafic2[table$date=='20170129'] # [1]  971869 1176429 2148298
table$trafic2[table$date=='20170130'] # [1]  932013 1092115 2024128

# 2017 추석 교통량 데이터 
table$trafic2[table$date=='20171002'] # [1] 1358391 1218056 2576447
table$trafic2[table$date=='20171003'] # [1] 1271103 1125741 2396844
table$trafic2[table$date=='20171004'] # [1] 1421458 1402145 2823603 추석 당일
table$trafic2[table$date=='20171005'] # [1] 1264337 1350042 2614379
table$trafic2[table$date=='20171006'] # [1] 1090897 1272370 2363267

# 2018 설날 교통량 데이터
table$trafic2[table$date=='20180215'] # [1] 1263171 1075020 2338191
table$trafic2[table$date=='20180216'] # [1] 1389264 1402362 2791626 설날 당일
table$trafic2[table$date=='20180217'] # [1] 1070535 1279801 2350336
table$trafic2[table$date=='20180218'] # [1]  921223 1092419 2013642

# 2018 추석 교통량 데이터
table$trafic2[table$date=='20180923'] # [1] 1279217 1091338 2370555
table$trafic2[table$date=='20180924'] # [1] 1455704 1460639 2916343 추석 당일
table$trafic2[table$date=='20180925'] # [1] 1185821 1404096 2589917
table$trafic2[table$date=='20180926'] # [1] 1038955 1239481 2278436

# 2019 설날 교통량 데이터
table$trafic2[table$date=='20190203'] # [1] 1023581  861636 1885217
table$trafic2[table$date=='20190204'] # [1] 1134309 1055514 2189823
table$trafic2[table$date=='20190205'] # [1] 1420881 1465577 2886458 설날 당일
table$trafic2[table$date=='20190206'] # [1] 1083538 1359293 2442831

# 2019 추석 교통량 데이터
table$trafic2[table$date=='20190912'] # [1] 1404786 1250205 2654991
table$trafic2[table$date=='20190913'] # [1] 1491021 1502611 2993632 추석 당일
table$trafic2[table$date=='20190914'] # [1] 1163062 1398367 2561429
table$trafic2[table$date=='20190915'] # [1] 1033412 1226440 2259852

# 2020 설날 교통량 데이터
table$trafic2[table$date=='20200124'] # [1] 1328715 1150771 2479486
table$trafic2[table$date=='20200125'] # [1] 1440113 1460428 2900541 설날 당일
table$trafic2[table$date=='20200126'] # [1] 1126027 1334949 2460976
table$trafic2[table$date=='20200127'] # [1]  938153 1083718 2021871


# 2017-2020 전체 시계열 시각화 
ggplot(table_in) + geom_line(aes(x = date2, y = trafic2, colour = year),show.legend = T)


# 입구량 명절 시각화

## 2017 설날
table_in_2017_month %>% filter(month==1) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[1]),colour = 'red')
## 2017 추석
table_in_2017_month %>% filter(month==10) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[1]),colour = 'red')

## 2018 설날
table_in_2018_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[2]),colour = 'red')
## 2018 추석
table_in_2018_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[2]),colour = 'red')

## 2019 설날
table_in_2019_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[3]),colour = 'red')
## 2019 추석
table_in_2019_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = in_trafic_year_summarise$trafic_mean[3]),colour = 'red')


# 출구량 명절 시각화

## 2017 설날
table_out_2017_month %>% filter(month==1) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[1]),colour = 'red')
## 2017 추석
table_out_2017_month %>% filter(month==10) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[1]),colour = 'red')

## 2018 설날
table_out_2018_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[2]),colour = 'red')
## 2018 추석
table_out_2018_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[2]),colour = 'red')

## 2019 설날
table_out_2019_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[3]),colour = 'red')
## 2019 추석
table_out_2019_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = out_trafic_year_summarise$trafic_mean[3]),colour = 'red')

# 합계량 명절 시각화

## 2017 설날
table_sum_2017_month %>% filter(month==1) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[1]),colour = 'red')
## 2017 추석
table_sum_2017_month %>% filter(month==10) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[1]),colour = 'red')

## 2018 설날
table_sum_2018_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[2]),colour = 'red')
## 2018 추석
table_sum_2018_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[2]),colour = 'red')

## 2019 설날
table_sum_2019_month %>% filter(month==2) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[3]),colour = 'red')
## 2019 추석
table_sum_2019_month %>% filter(month==9) %>%
  ggplot(aes(x = date2, y = trafic2)) + geom_line() +geom_point() +geom_line(aes(y = sum_trafic_year_summarise$trafic_mean[3]),colour = 'red')


# 각 년도 월별 빈도수 시각화 













