drop table if exists users;
create table users (
  user_id integer primary key autoincrement,
  username text not null,
  password text not null
);
