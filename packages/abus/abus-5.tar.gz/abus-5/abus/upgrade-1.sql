-- upgrade *from* schema 1 to latest (currently 3)

-- using non-null default values for archive_dir and is_compresed, will be updated by special case in python
update run
   set is_complete= case when timestamp is not null then 1 else 0 end
      ,archive_dir= ''
      ,timestamp= null
      ;
update location set is_compressed= 0;
