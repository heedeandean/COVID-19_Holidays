create table Exam (
	exam_id int(11) primary key, 
	statedt varchar(13), 				-- 기준일
    	decidecnt int(13),				-- 확진자 수 
    	deathcnt int(13),				-- 사망자 수 
	clearcnt int(13),				-- 격리해제 수
    	examcnt int(13),				-- 검사진행 수
    	carecnt int(13),				-- 치료중인 환자 수
    	resutlnegcnt int(20),				-- 결과 음성 수
    	accexamcnt int(20),				-- 누적 검사 수
    	accexamcompcnt int(20),  			-- 누적 검사 완료 수
    	accdefrate float(20),			 	-- 누적 확진률	
    	createdate  timestamp not null DEFAULT CURRENT_TIMESTAMP  
);

create table GGInfo (
	gginfo_id int(11) primary key, 	-- 연번
	loc varchar(128), 		-- 지역
    	how_inf varchar(4096),		-- 발생경위
    	relation varchar(4096),		-- 관련성    
    	gender varchar(5),		-- 성별
    	age varchar(5),			-- 나이(만)
    	age_group varchar(5),		-- 연령대
    	cfm_date varchar(13),		-- 확진일
    	symptom_date varchar(13),	-- 증상발현일
	issymtom varchar(4096),		-- 증상 유무
    	route varchar(4096),		-- 감염경로
    	createdate  timestamp not null DEFAULT CURRENT_TIMESTAMP  
);

describe GGInfo;
drop table Exam;
select * from Exam;
delete from Exam;
