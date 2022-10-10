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
	company text not null,
	v_type text not null, 
	weight_amount int(3) not null,
	start datetime not null,
	foreign key (customer_id) references users (id),
	foreign key (company) references users (comp_name)
);
