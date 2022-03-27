drop table if exists contacts;
create table contacts (
	id INTEGER NOT NULL PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(120),
	phone VARCHAR(30),
	created DATE
);
