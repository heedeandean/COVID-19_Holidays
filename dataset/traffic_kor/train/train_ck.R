# 경기도 데이터 확인하기 #
# 1) 필요한 데이터만 추출.
# - cvs 읽어오기
dt2017 <- read.csv('c:/workspaces/COVID_19/train2017_gg.csv')
dt2018 <- read.csv('c:/workspaces/COVID_19/train2018_gg.csv')
dt2019 <- read.csv('c:/workspaces/COVID_19/train2019_gg.csv')
dt2020 <- read.csv('c:/workspaces/COVID_19/train2020_gg.csv')

# 데이터 합치기
dt_all <- rbind(dt2017,dt2018,dt2019,dt2020)
View(dt_all)
write.csv(dt_all, 'c:/workspaces/COVID_19/train_all_gg.csv')

# - 변수명 바꾸기
dt_all <- rename(dt_all,
                 month = '연월',
                 ktx_alight = 'KTX_하차수.명.',
                 sm_alight = '새마을_하차수.명.',
                 mg_alight = '무궁화_하차수.명..',
                 nr_alight ='누리로_하차수.명.',
                 ktx_sc_alight = 'KTX산천_하차수.명.',
                 itx_sm_alight = 'ITX새마을_하차수.명.',
                 itx_youth_alight = 'ITX청춘열차_하차수.명.',
                 ktx_hn_alight = 'KTX호남_하차수.명.')

# - 필요한 데이터만 추출하기
train_1 <- dt_all %>%
  select(month, station,ktx_alight,,sm_alight,mg_alight,nr_alight,ktx_sc_alight,ktx_hn_alight,itx_sm_alight,itx_youth_alight) 
View(train_1)  
train_sum <- train_1 %>% 
  select(ktx_alight,,sm_alight,mg_alight,nr_alight,ktx_sc_alight,ktx_hn_alight,itx_sm_alight,itx_youth_alight)
train_1$total <- rowSums(train_sum)

train_2 <- train_1 %>% 
  group_by(month) %>%
  summarise(month_total = sum(total))
View(train_2)

# - 간단한 시각화를 하여 비교
# 년도별 
train17 <- as.data.frame(train_2[grep(2017,train_2$month),])
train18 <- train_2[grep(2018,train_2$month),]
train19 <- train_2[grep(2019,train_2$month),]
train20 <- train_2[grep(2020,train_2$month),]
#View(train17)
#ggplot(data=train17,aes(x=month, y=month_total))+geom_bar()+ylim(1000000,1500000)

#par(mfrow=c(2,2))
x11()
ggplot(data=train17,aes(x=month, y=month_total))+geom_line()
ggplot(data=train18,aes(x=month, y=month_total))+geom_line()
ggplot(data=train19,aes(x=month, y=month_total))+geom_line()
ggplot(data=train20,aes(x=month, y=month_total))+geom_line()






