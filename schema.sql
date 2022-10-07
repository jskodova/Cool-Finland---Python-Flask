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

create table deliveriestest (
	id integer primary key autoincrement,
	customer_id integer,
	title text not null,
	v_type text not null, 
	weight_amount float(3) not null,
	start datetime not null,
	foreign key (customer_id) references users (id),
	foreign key (title) references users (comp_name)
);


INSERT INTO deliveriestest (id, customer_id, title, v_type, weight_amount, start)
VALUES (1,1,"Revisol Oy","small truck",50,"2022-10-24");

INSERT INTO deliveriestest (id, customer_id, title, v_type, weight_amount, start)
VALUES (2,2,"Kuonepeikko Oy","small truck",50,"2022-10-10");


INSERT INTO deliveriestest (id, customer_id, title, v_type, weight_amount, start)
VALUES (3,3,"Tavastia","small truck",80,"2022-10-01");
