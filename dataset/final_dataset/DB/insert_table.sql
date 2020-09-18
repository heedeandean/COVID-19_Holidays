-- 해외
insert into GGExternal(cfm_date, cfm_cnt, cum_cfm_cnt)
(select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
  from ( select cfm_date, count(*) as cfm_cnt
			 from gginfo
			 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%'
			 group by cfm_date) as a,  (Select @total := 0) as total);
			

-- 614/3475 = 4089
-- 국내
  select *
    from gginfo 
    where gginfo_id not in (select gginfo_id
									 from gginfo 
									 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%');
                       
                       
 -- 유                      
  select cfm_date, count(*) as symptom
    from gginfo
    where gginfo_id not in (select gginfo_id
									 from gginfo 
									 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = ''
	group by cfm_date;

 
 -- 무
  select cfm_date, count(*) as asymptom
    from gginfo
    where gginfo_id not in (select gginfo_id
									 from gginfo 
									 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '무증상'
	group by cfm_date;
    
    
 -- 조사중    
    select cfm_date, count(*) as research
    from gginfo
    where gginfo_id not in (select gginfo_id
									 from gginfo 
									 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '조사중'
	group by cfm_date;

  
  -- 유 : 2414 / 무 : 1029 / 조 : 32
  
  
select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
  from (select cfm_date, count(*) as cfm_cnt
			from gginfo 
			where gginfo_id not in (select gginfo_id
											  from gginfo 
											  where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%')
			group by cfm_date) as a,  (Select @total := 0) as total;
            
            
-- 국내 총 결과            
 select AA.cfm_date, BB.symptom, CC.asymptom, DD.research, AA.cfm_cnt, AA.cum_cfm_cnt, EE.exam_cnt
   from (select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
			 from (select cfm_date, count(*) as cfm_cnt
					   from gginfo 
					   where gginfo_id not in (select gginfo_id
														 from gginfo 
														 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%')
					   group by cfm_date) as a,  (Select @total := 0) as total) as AA 
			LEFT JOIN (select cfm_date, count(*) as symptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = ''
																group by cfm_date) as BB ON (AA.cfm_date = BB.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as asymptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '무증상'
																group by cfm_date) as CC ON (AA.cfm_date = CC.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as research
							 from gginfo
							 where gginfo_id not in (select gginfo_id
															  from gginfo 
															  where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '조사중'
															  group by cfm_date) as DD ON (AA.cfm_date = DD.cfm_date) 
			LEFT JOIN (select * from exam) as EE ON (AA.cfm_date = EE.exam_date);
            
            
 insert into GGInternal(cfm_date, symptom, asymptom, research, cfm_cnt, cum_cfm_cnt, exam_cnt)
(select AA.cfm_date, BB.symptom, CC.asymptom, DD.research, AA.cfm_cnt, AA.cum_cfm_cnt, EE.exam_cnt
   from (select cfm_date, cfm_cnt, @total := @total + cfm_cnt as cum_cfm_cnt
			 from (select cfm_date, count(*) as cfm_cnt
					   from gginfo 
					   where gginfo_id not in (select gginfo_id
														 from gginfo 
														 where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%')
					   group by cfm_date) as a,  (Select @total := 0) as total) as AA 
			LEFT JOIN (select cfm_date, count(*) as symptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = ''
																group by cfm_date) as BB ON (AA.cfm_date = BB.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as asymptom
							  from gginfo
							  where gginfo_id not in (select gginfo_id
																from gginfo 
																where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '무증상'
																group by cfm_date) as CC ON (AA.cfm_date = CC.cfm_date) 
			LEFT JOIN (select cfm_date, count(*) as research
							 from gginfo
							 where gginfo_id not in (select gginfo_id
															  from gginfo 
															  where route = '해외유입' or how_inf like '%해외%' or relation like '%해외%') and issymtom = '조사중'
															  group by cfm_date) as DD ON (AA.cfm_date = DD.cfm_date) 
			LEFT JOIN (select * from exam) as EE ON (AA.cfm_date = EE.exam_date)); 
