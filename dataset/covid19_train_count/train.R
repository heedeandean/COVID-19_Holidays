## 2017 자료
data1 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201701.xlsx')
data2 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201702.xlsx')
data3 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201703.xlsx')
data4 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201704.xlsx')
data5 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201705.xlsx')
data6 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201706.xlsx')
data7 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201707.xlsx')
data8 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201708.xlsx')
data9 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201709.xlsx')
data10 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201710.xlsx')
data11 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201711.xlsx')
data12 <- read_excel('C:/Users/aej32/Downloads/project/train/train2017/201712.xlsx')

# 데이터 합치기
data2017 <- rbind(data1, data2, data3, data4, data5, data6, data7, data8,data9,data10,data11,data12)
write.csv(data2017, "c:/workspaces/COVID_19/train2017_all.csv", row.names = FALSE)
table(is.na(data2017))
View(data2017)
str(data2017)

# 데이터 1차 가공 - 경기도 자료만
data2017_2 <- data2017
data2017_2 <- rename(data2017_2, station = '역명/열차종별')
data2017_2 <- data2017_2 %>%
  filter(station %in% c("가평","광명","능곡","대광리","덕소","덕정"
                      ,"도농","도라산","동두천","동두천중앙","동탄(SRT)"
                      ,"마석","매곡","문산","백마","삼산","서정리","석불"
                      ,"소요산","수원","신망리","신탄리","안산","안양","양동"
                      ,"양수","양평","연천","오산","용문","운천","의왕","의정부"
                      ,"일산","일신","임진강","전곡","중동","지제(SRT)","지평"
                      ,"초성리","퇴계원","평내호평","평택","한탄강","행신"))
View(data2017_2)

write.csv(data2017_2, "c:/workspaces/COVID_19/train2017_gg.csv", row.names = FALSE)



# 2018년도 자료
data1 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201801.xlsx')
data2 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201802.xlsx')
data3 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201803.xlsx')
data4 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201804.xlsx')
data5 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201805.xlsx')
data6 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201806.xlsx')
data7 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201807.xlsx')
data8 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201808.xlsx')
data9 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201809.xlsx')
data10 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201810.xlsx')
data11 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201811.xlsx')
data12 <- read_excel('C:/Users/aej32/Downloads/project/train/train2018/201812.xlsx')

# 데이터 합치기
data2018 <- rbind(data1, data2, data3, data4, data5, data6, data7, data8,data9,data10,data11,data12)
write.csv(data2018, "c:/workspaces/COVID_19/train2018_all.csv", row.names = FALSE)
table(is.na(data2018))
View(data2018)
str(data2018)

data2018_2 <- data2018
data2018_2 <- rename(data2018, station = '역명/열차종별')
data2018_2 <- data2018_2 %>%
  filter(station %in% c("가평","광명","능곡","대광리","덕소","덕정"
                        ,"도농","도라산","동두천","동두천중앙","동탄(SRT)"
                        ,"마석","매곡","문산","백마","삼산","서정리","석불"
                        ,"소요산","수원","신망리","신탄리","안산","안양","양동"
                        ,"양수","양평","연천","오산","용문","운천","의왕","의정부"
                        ,"일산","일신","임진강","전곡","중동","지제(SRT)","지평"
                        ,"초성리","퇴계원","평내호평","평택","한탄강","행신"))
View(data2018_2)
write.csv(data2018_2, "c:/workspaces/COVID_19/train2018_gg.csv", row.names = FALSE)



# 2019년도 자료
data1 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201901.xlsx')
data2 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201902.xlsx')
data3 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201903.xlsx')
data4 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201904.xlsx')
data5 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201905.xlsx')
data6 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201906.xlsx')
data7 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201907.xlsx')
data8 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201908.xlsx')
data9 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201909.xlsx')
data10 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201910.xlsx')
data11 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201911.xlsx')
data12 <- read_excel('C:/Users/aej32/Downloads/project/train/train2019/201912.xlsx')

# 데이터 합치기
data2019 <- rbind(data1, data2, data3, data4, data5, data6, data7, data8,data9,data10,data11,data12)
write.csv(data2019, "c:/workspaces/COVID_19/train2019_all.csv", row.names = FALSE)
table(is.na(data2019))
View(data2019)
str(data2019)

data2019_2 <- data2019
data2019_2 <- rename(data2019, station = '역명/열차종별')
data2019_2 <- data2019_2 %>%
  filter(station %in% c("가평","광명","능곡","대광리","덕소","덕정"
                        ,"도농","도라산","동두천","동두천중앙","동탄(SRT)"
                        ,"마석","매곡","문산","백마","삼산","서정리","석불"
                        ,"소요산","수원","신망리","신탄리","안산","안양","양동"
                        ,"양수","양평","연천","오산","용문","운천","의왕","의정부"
                        ,"일산","일신","임진강","전곡","중동","지제(SRT)","지평"
                        ,"초성리","퇴계원","평내호평","평택","한탄강","행신"))
View(data2019_2)
write.csv(data2019_2, "c:/workspaces/COVID_19/train2019_gg.csv", row.names = FALSE)



# 2020년도 자료
data1 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202001.xlsx')
data2 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202002.xlsx')
data3 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202003.xlsx')
data4 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202004.xlsx')
data5 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202005.xlsx')
data6 <- read_excel('C:/Users/aej32/Downloads/project/train/train2020/202006.xlsx')


# 데이터 합치기
data2020 <- rbind(data1, data2, data3, data4, data5, data6)
write.csv(data2020, "c:/workspaces/COVID_19/train2020_all.csv", row.names = FALSE)
table(is.na(data2020))
View(data2020)
str(data2020)

data2020_2 <- data2020
data2020_2 <- rename(data2020, station = '역명/열차종별')
data2020_2 <- data2020_2 %>%
  filter(station %in% c("가평","광명","능곡","대광리","덕소","덕정"
                        ,"도농","도라산","동두천","동두천중앙","동탄(SRT)"
                        ,"마석","매곡","문산","백마","삼산","서정리","석불"
                        ,"소요산","수원","신망리","신탄리","안산","안양","양동"
                        ,"양수","양평","연천","오산","용문","운천","의왕","의정부"
                        ,"일산","일신","임진강","전곡","중동","지제(SRT)","지평"
                        ,"초성리","퇴계원","평내호평","평택","한탄강","행신"))
View(data2020_2)
write.csv(data2020_2, "c:/workspaces/COVID_19/train2020_gg.csv", row.names = FALSE)






