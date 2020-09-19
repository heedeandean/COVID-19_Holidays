# install.packages('RMySQL')
library(RMySQL)

drv = dbDriver("MySQL")
conn_covid = dbConnect(drv, host='127.0.0.1', port=3306, 
                     dbname='covid19', user='root', password='1234')
dbSendQuery(conn_covid, 'set character set utf8') 
dbListTables(conn_covid)   

mg = dbGetQuery(conn_covid, "select * from ggexternal;")
mg
