gg_df <- read.csv("C:/Users/user/Desktop/cov/gg0827.csv")

# 필요한 데이터만 추출
gg <- gg_df[,c(1,6,12,13)]
names(gg) <- c("area","cfmDate","route","contactCnt")
gg$area <- "경기도"
gg$contactCnt <- "-"
gg$cfmDate <- gsub("[[:punct:]]","-",gg$cfmDate)
gg$cfmDate <- as.Date(gg$cfmDate)


# 성별, 연령대 데이터 추가
gg$gender <- gg_df[,3]
gg$age <- gg_df[,5]
gg$age <- paste0(gg$age,"s")

gg <- gg %>% arrange(cfmDate)

View(gg)



# 구분(접촉자)포함 데이터추출
gg2 <- gg
gg2$contact <- gg_df[,15]

gg2 <- gg2 %>% arrange(cfmDate)

View(gg2)

write.csv(gg, 'C:/Users/user/Desktop/cov/gg_200828.csv', row.names = F)
write.csv(gg2,'C:/Users/user/Desktop/cov/gg2_200828.csv', row.names = F)




