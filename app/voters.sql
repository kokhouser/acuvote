delete from voters;
insert into voters (fname,lname,username,class,isadmin) values ("Jonathan","Nix","jrn11a","SR",0);
insert into voters (fname,lname,username,class,isadmin) values ("Jeremy","Ron","jir13b","JR",0);
insert into voters (fname,lname,username,class,isadmin) values ("Claire","DuCanoe","cod42o","SO",0);
insert into voters (fname,lname,username,class,isadmin) values ("Marker","Pason","map21a","FR",1);
delete from elections;
insert into elections (name) values ("President")
insert into elections (name) values ("Vice President")
delete from candidates;
insert into candidates (electionid,voterid,position,votes) values (1,1,"President",0)
insert into candidates (electionid,voterid,position,votes) values (2,1,"President",0)
insert into candidates (electionid,voterid,position,votes) values (1,1,"President",0)
insert into candidates (electionid,voterid,position,votes) values (1,1,"President",0)
insert into candidates (electionid,voterid,position,votes) values (1,1,"President",0)
insert into candidates (electionid,voterid,position,votes) values (1,1,"President",0)