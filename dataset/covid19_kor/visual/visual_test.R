library(readr)
library(dplyr)
library(ggplot2)
install.packages("corrplot")
library(corrplot)

getwd()
nation <- read_csv("./cnt/nation_API_cnt_2020_09_12.csv")
View(nation)

# nation_0302 = subset(x = nation, statedt >= '2020-03-01')

# View(nation_0302)

for (i in 1:nrow(nation)){
  nation[i,'def_date'] = nation[i,"decidecnt"] - nation[i+1,"decidecnt"]
  nation[i,'neg_date'] = nation[i,"resutlnegcnt"] - nation[i+1,"resutlnegcnt"]
}
View(nation)

nation_0303 = subset(x = nation, statedt >= '2020-03-03')

View(nation_0303)

nation_0303 %>% 
  ggplot(aes(x=examcnt, y=def_date)) +
    ylab("일별 확진자") +
    xlab("일별 검사") +
    geom_point() +
    geom_smooth(method="lm", se=FALSE)


examcnt <- nation_0303$examcnt
def_date <- nation_0303$def_date

CrossTable(examcnt , def_date ,chisq = T)

nation %>% 
  ggplot(aes(x=seq, y=examcnt)) +
  ylab("일별 확진자") +
  xlab("시간") +
  geom_line() 
cor_nation <- nation %>% select(decidecnt,examcnt,def_date) 

cor_nation_0303 <- nation_0303 %>% select(-c(statedt,X1,seq))
corrgram(cor_nation)
corrgram(cor_nation_0303, lower.panel = panel.conf)


nation_exam <- nation %>%  select(statedt,examcnt,accexamcnt,accexamcompcnt)

write.csv(nation_exam,file = 'nation_exam.csv')

exam_cor <- read.csv('C:/Users/tjoeun/Desktop/nation_exam_plus.csv')
exam_cor$examcnt <- as.integer(exam_cor$examcnt)
exam_cor$statedt <- as.Date.character(exam_cor$statedt)

exam_cor <- subset(exam_cor, statedt>='2020-03-03')
exam_cor <- exam_cor %>% select(-statedt)
exam_cor$neg_date <- nation_0303$neg_date

M <- cor(exam_cor)
M2 <- nation %>% filter(statedt>='2020-03-03') %>% select(-c(statedt,X1,seq)) %>% cor()

nation_t <- nation %>% filter(statedt>='2020-03-03') %>% select(-c(statedt,X1,seq))

str(exam_cor)
View(exam_cor)

col4 <- colorRampPalette(c("#7F0000", "red", "#FF7F00", "yellow", "#7FFF7F", 
                           "cyan", "#007FFF", "blue", "#00007F"))


corrgram(exam_cor, upper.panel=panel.conf)

corrplot(M, order = "hclust", addrect = 2, method="number")

corrplot.mixed(M2,lower="ellipse",upper="number")

pairs(nation_t)

policy <- read.csv('C:/Users/tjoeun/Desktop/gg_0909.csv')

View(policy)
