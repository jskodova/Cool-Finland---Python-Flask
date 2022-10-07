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


INSERT INTO deliveries (id, customer_id, company, v_type, weight_amount, start)
VALUES (1,1,"Revisol Oy","small truck",50,"2022-10-24");

INSERT INTO deliveries (id, customer_id, company, v_type, weight_amount, start)
VALUES (2,2,"Kuonepeikko Oy","small truck",50,"2022-10-10");


INSERT INTO deliveries (id, customer_id, company, v_type, weight_amount, start)
VALUES (3,3,"Tavastia","small truck",20,"2022-10-15");
