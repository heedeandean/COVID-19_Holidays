# chap09_FormalInformal

########################################
# chapter09. 정형 / 비정형 데이터 처리
########################################

## 1.1 Oracle 정형 데이터 처리
# 단계1: 사용자 로그인과 테이블 생성.
# -sqlplus 명령문으로 접속 후 다음의 테이블 생성.
# """ 또는 ''' 로 사용가능. 문자열을 처리.- 주석효과

"""
SQL>
create table test_table(
  id    varchar2(50)    primary key,
  pass  varchar2(30)    not null,
  name  varchar2(30)    not null,
  age   number(2)
);

"""

# 단계2 : 레코드 추가와 조회하기
# SQL> insert into test_table values('hong', '1234', '홍길동',25);
# SQL> insert into test_table values('lee', '1234', '이순신',30);

# 단계3 : transaction 처리 -commit;
# SQL> commit;


# Oracle 연동을 위한 R패키지 설치.
# 1) 패키지 설치
# - RJDBC패키지를 사용하기 위해서는 우선 java를 설치해야 한다.
install.packages("rJava")
install.packages("DBI")
install.packages("RJDBC")

# 2) 패키지 로딩
Sys.setenv(JAVA_HOME='C:/Program Files/Java/jre1.8.0_221')
library(DBI)
library(rJava)
library(RJDBC) # rJava에 의존적이다.(rJava 먼저 로딩).

# 3) Oracle 연동
### Oracle 11g Ex.
# driver
drv <- JDBC("oracle.jdbc.driver.OracleDriver", 
     "C:/oraclexe/app/oracle/product/11.2.0/server/jdbc/lib/ojdbc6_g.jar")

# db연동(driver, url, id, pwd)
conn <- dbConnect(drv, "jdbc:oracle:thin:@//localhost:1521/xe", "scott", "tiger")

# (1) 모든 레코드 검색
query <- "select * from test_table"
dbGetQuery(conn, query)

# (2) 조건 검색 - 나이가 30세 이상인 레코드 조회
query <- "select * from test_table where age >= 30"
result <- dbGetQuery(conn, query) # 검색결과 변수에 보관관
result
str(result) # 'data.frame':	1 obs. of  4 variables:
View(result)


# (3) 정렬 조회 - 나이 컬럼을 기준으로 내림차순 정렬
query <- "select * from test_table order by age desc"
dbGetQuery(conn, query)


# (4) 레코드 삽입
query <- "insert into test_table values('kang', '1234', '강감찬', 35)"
dbSendUpdate(conn, query) # R은 삽입시 이 함수 사용해야함
query <- "select * from test_table" # 확인용
dbGetQuery(conn, query)


# (5) 레코드 수정 - 데이터 '강감찬'의 나이를 40으로 수정.
query <- "update test_table set age=40 where name='강감찬' "
# ""안에 ""를 사용하면 오류남.
dbSendUpdate(conn, query)
query <- "select * from test_table"
dbGetQuery(conn, query)


# (6) 레코드 삭제 - 데이터 '홍길동' 레코드 삭제
query <- "delete from test_table where name='홍길동'"
dbSendUpdate(conn, query)  # RJDBC패키지가 제공.
query <- "select * from test_table"
dbGetQuery(conn, query)


# (7) db 연결 종료
dbDisconnect(conn) # DBI에서 제공


# 2. 비정형 데이터 처리 (텍스트 마이닝 분석)
# - 텍스트 마이닝(Text Mining) : 문자로 된 데이터에서 가치 있는 정보를 얻어 내는 분석기법.

## 2.1 토픽 분석
# - 텍스트 데이터를 대상으로 단어를 추출하고, 이를 단어사전과 비교하여 단어의 출현  빈도수를 분석하는 텍스트 마이닝 분석과정을 의미.
# - 또한 단어 구름(word cloud) 패키지를 적용하여 분석 결과를 시각화하는 과정도 포함.

# (1) 패키지 설치 및 준비
install.packages("KoNLP") # 원래 필요한 패키지
# - package ‘KoNLP’ is not available (for R version 4.0.1)

install.packages("https://cran.rstudio.com/bin/windows/contrib/3.4/KoNLP_0.80.1.zip",
                 repos = NULL)
# package ‘KoNLP’ successfully unpacked and MD5 sums checked - 설치 완료

# Sejong 설치 : KoNLP와 의존성 있는 현재 버전의 한글 사전 패키지 설치
install.packages("Sejong")
install.packages(c("hash","tau","RSQLite", "rJava", "devtools"))

library(Sejong)
library(hash)
library(tau)
library(RSQLite)
Sys.setenv(JAVA_HOME='C:/Program Files/Java/jre1.8.0_221')
library(rJava)
library(devtools)
library(KoNLP)















