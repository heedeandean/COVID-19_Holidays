describe gginternal;
select * from Exam order by 1 desc;
select * from GGInfo order by gginfo_id desc; 
-- drop table GGExternal;
-- delete from Exam;

-- route = '해외유입' 인데 국내로 분류된 것
select * from gginfo where gginfo_id not in (
select gginfo_id from GGInfo where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국') and route = '해외유입';

-- 국내
select * from gginfo where gginfo_id not in (
select gginfo_id from GGInfo where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국'); 

-- 해외
select * from GGInfo where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국';


-- 경기도 못가져온 데이터 있는지 확인
select * from gginfo where loc is null and how_inf is null and relation is null;

