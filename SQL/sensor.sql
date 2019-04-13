create table sensor
(
  id varchar(127) not null primary key,
  name varchar(255) not null default 'sensor',
  location varchar(255) default 'Комната'
)