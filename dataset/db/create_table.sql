create table Coronic (
	coronic_id int unsigned not null auto_increment primary key,
    area varchar(128) not null,
    cfm_date varchar(13),
    route varchar(4096),
    contact_cnt varchar(5),
    gender varchar(5),
    age varchar(5),
    create_date  timestamp not null DEFAULT CURRENT_TIMESTAMP
);

drop table Coronic;

select * from coronic;

delete from coronic;