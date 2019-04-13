create table sensor_value (
  id serial not null primary key,
  value smallint,
  sensor varchar(127) not null,
  date timestamp default now()
)