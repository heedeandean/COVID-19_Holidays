# 제공 url
base_url <- "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson"

# 인증키와 그외 정보
key <- "sA78yY%2FijK3uskzaHrmoktsxRUj05qXiFwAnVayPUdTBcDb2CoejuL1GSJp0pp%2FwItgI2pPV2VGKpxzSDX8%2BYA%3D%3D"
rows <-  10
pg <- 1
startdate <- 20200101
enddate <- 20200821

# 오픈 API호출 url생성
url <- paste0(base_url,paste0("?serviceKey=",key),paste0('&numOfRows=',rows),paste0('&startCreateDt=',startdate),
              paste0('&endCreateDt=',enddate),paste0('&pageNo=',pg))

# 호출
doc <- xmlTreeParse(url, useInternalNodes = TRUE, encoding = "UTF-8")

# xml 루트노드 획득- r에서 xml데이터를 처리하기 위해 root node에 접근
rootNode <- xmlRoot(doc)

# 호출결과 데이터 개수 획득 - xpathsapply()로 xml데이터 내에서 특정 node의 데이터를 읽어옴
numofRow <- as.numeric(xpathSApply(rootNode, "//numOfRows", xmlValue)) # numofrows변수에 저장

# 전체 데이터의 개수 획득
totalcount <- as.numeric(xpathSApply(rootNode, "//totalCount", xmlValue))

# 총 오픈api 호출횟수 계산 - 전체데이터개수에서 오픈api호출결과 데이터개수로 나누면 오픈api의 총 호출횟수 계산가능
loopCount <- round(totalcount/numofRow, 0)

# api호출횟수 보정
# 호출횟수만큼 반복 후출하여 모든 데이터를 획득.1씩증가하도록
if(loopCount*numofRow < totalcount){
  loopCount <- loopCount+1
}

# 전체 데이터를 저장할 변수 선언
totalData <- data.frame()

# dataframe으로 저장
xmlData <- xmlToDataFrame(nodes = getNodeSet(rootNode,'//item'))
totalData <- rbind(totalData,xmlData)

# 데이터 확인
View(totalData)

# csv파일로 저장
write.csv(totalData, "c:/workspaces/R/COVID_19/covid19_0821.csv", row.names=FALSE)


