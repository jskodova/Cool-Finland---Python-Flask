drop table if exists users;
drop table if exists deliveries;


create table users (
 	id integer primary key autoincrement,
 	email text not null,
 	password text not null,
 	comp_name text not null,
 	rep_name text not null,
 	rep_lname text not null,
 	rep_pnumber text not null,
 	priority bool
);


create table deliveries (
	id integer primary key autoincrement,
	customer_id integer,
	weight_amount float(3) not null,
	delivery_date date not null,
	foreign key (customer_id) references users (id)
);