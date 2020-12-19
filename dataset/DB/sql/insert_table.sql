-- 국내
delete from GGInternal;
 insert into GGInternal(cfm_date, symptom, asymptom, research, cfm_cnt, cum_cfm_cnt, exam_cnt)
(select AA.cfm_date, ifnull(BB.symptom, 0), ifnull(CC.asymptom, 0), ifnull(DD.research, 0), AA.cfm_cnt, AA.cum_cfm_cnt, EE.exam_cnt
   from (select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
			 from (select cfm_date, count(*) as cfm_cnt
					   from gginfo 
					   where gginfo_id not in (select gginfo_id
														 from gginfo 
														 where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국')
					   group by cfm_date) as a,  (Select @total := 0) as total) as AA 
			LEFT JOIN (select cfm_date, count(*) as symptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국') and issymtom = ''
																group by cfm_date) as BB ON (AA.cfm_date = BB.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as asymptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국') and issymtom = '무증상'
																group by cfm_date) as CC ON (AA.cfm_date = CC.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as research
							 from gginfo
							 where gginfo_id not in (select gginfo_id
															  from gginfo 
															  where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국') and issymtom = '조사중'
															  group by cfm_date) as DD ON (AA.cfm_date = DD.cfm_date) 
			LEFT JOIN exam as EE ON (AA.cfm_date = EE.exam_date)); 

-- 정책
-- 2020-01-26 ~ 2020-03-21 => 0
-- 2020-03-22 ~ 2020-04-19 => 1.5
-- 2020-04-20 ~ 2020-08-17 => 1
-- 2020-08-18 ~ 2020-08-29 => 2
-- 2020-08-30 ~ 2020-09-13 => 2.5
-- 2020-09-14 ~ 현재 => 2

update GGInternal
	set policy = 0
    where cfm_date between '2020-01-26' and '2020-03-21';

update GGInternal
	set policy = 1.5
    where cfm_date between '2020-03-22' and '2020-04-19';
    
update GGInternal
	set policy = 1
    where cfm_date between '2020-04-20' and '2020-08-17';    
    
update GGInternal
	set policy = 2
    where cfm_date between '2020-08-18' and '2020-08-29';  
    
update GGInternal
	set policy = 2.5
    where cfm_date between '2020-08-30' and '2020-09-13';  
    
update GGInternal
	set policy = 2
    where cfm_date between '2020-09-14' and (select * from (select max(cfm_date) from gginternal) as aa);      
    
    

-- 해외

-- insert into GGExternal(cfm_date, cfm_cnt, cum_cfm_cnt)
-- (select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
--   from ( select cfm_date, count(*) as cfm_cnt
-- 			 from gginfo
-- 			 where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국'
-- 			 group by cfm_date) as a,  (Select @total := 0) as total);
-- 

delete from filldates;
CALL filldates((select min(cfm_date) from gginfo), (select max(cfm_date) from gginfo));

delete from GGExternal;
insert into GGExternal(cfm_date, cfm_cnt, cum_cfm_cnt)
(select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
   from (select f.cfm_date, ifnull(cfm_cnt, 0) as cfm_cnt 
		  from filldates as f 
	 LEFT JOIN (select cfm_date, count(*) as cfm_cnt
				 from gginfo
				 where how_inf REGEXP '유럽|해외|입국|비행기|태국|이란' or relation REGEXP '유럽|해외|입국|비행기|태국'
				 group by cfm_date) as g ON (f.cfm_date = g.cfm_date)) as t
	    , (Select @total := 0) as total);

    
-- 데이터 확인    
select * from gginternal where policy is null;
select * from GGInternal order by 1 desc;
select * from GGExternal order by 1 desc;

-- 574 / 3650 4224