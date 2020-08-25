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
write.csv(se, 'C:/Users/user/Desktop/cov/se200824.csv',row.names = F)
