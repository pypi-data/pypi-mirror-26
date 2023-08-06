-- upgrade *from* schema 2 to latest (currently 3)

-- using non-null default values for archive_dir and is_compresed, will be updated by special case in python
update location set is_compressed= 0;
insert into run(run_name, is_complete, archive_dir)
   select run_name, 1, ''
   from completed_run
   ;
insert into run(run_name, is_complete, archive_dir)
   select distinct run_name, 0, ''
   from content
   where run_name not in(select run_name from completed_run)
   ;
delete from completed_run;

