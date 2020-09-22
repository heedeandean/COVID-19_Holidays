create table Exam (
	exam_date varchar(13) primary key,  -- 검사 일
    	exam_cnt int(13),		    -- 검사 수
    	create_date  timestamp not null DEFAULT CURRENT_TIMESTAMP  
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
    	create_date  timestamp not null DEFAULT CURRENT_TIMESTAMP  
);

-- 국내
create table GGInternal (
    cfm_date varchar(13) primary key,	 	-- 확진일
    symptom int(13),				-- 유증상
    asymptom int(13),				-- 무증상
    research int(13),				-- 조사중
    cfm_cnt int(13),				-- 당일 확진자 수
    cum_cfm_cnt  int(20),			-- 누적 확진자 수
    exam_cnt int(13),				-- 검사 수
    policy float(20),				-- 정책
    create_date  timestamp not null DEFAULT CURRENT_TIMESTAMP  
);

-- 해외
drop table if exists GGExternal;

create table GGExternal (
    cfm_date varchar(13) primary key,	 -- 확진일
    cfm_cnt int(13),			 -- 당일 확진자 수
    cum_cfm_cnt  int(20),		 -- 누적 확진자 수
    create_date  timestamp not null DEFAULT CURRENT_TIMESTAMP  
);


create table FillDates (
    cfm_date varchar(13) primary key
);


