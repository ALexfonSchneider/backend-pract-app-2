CREATE TABLE users (
	id serial PRIMARY KEY,
	first_name text,
	last_name text,
	email text,
	join_date timestamp default current_date,
	password_hash text
);


CREATE TABLE tasks (
	id serial PRIMARY KEY,
	user_id integer,
	description text,
	closed boolean,

	CONSTRAINT fr_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);
