drop table if exists voters;
create table voters (
  id integer primary key,
  fname text not null,
  lname text not null,
  username text not null,
  -- reshallid integer not null,
  class text not null,
  isadmin boolean not null
  -- foreign key(reshallid) references reshalls(id)
);

drop table if exists reshalls;
create table reshalls (
	id integer primary key autoincrement,
	name text
);

drop table if exists departments;
create table departments (
	id integer primary key autoincrement,
	name text
);

drop table if exists voter_dpt;
create table voter_dpt (
	id integer primary key autoincrement,
	depid integer,
	voterid integer,
	foreign key (depid) references departments(id),
	foreign key (voterid) references voters(id)
);

drop table if exists elections;
create table elections (
	id integer primary key autoincrement,
	name text not null
);

drop table if exists candidates;
create table candidates (
	id integer primary key autoincrement,
	electionid integer,
	voterid integer,
	position text not null,
	votes integer,
	foreign key (electionid) references elections(id),
	foreign key (voterid) references voters(id)
);
