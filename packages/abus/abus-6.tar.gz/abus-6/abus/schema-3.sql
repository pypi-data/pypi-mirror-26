-- schema 3, ABuS v5 v6

create table content(
   run_name text not null,
   path text not null,
   timestamp float not null,
   checksum text not null);
create unique index content_pk on content(run_name, path);
create index content_path on content(path);

create table location(
   checksum text not null,
   is_compressed int not null,
   archive_dir text not null);
create unique index location_pk on location(checksum);
create index location_archivedir on location(archive_dir);

create table checksum_cache(
   dev int not null,
   ino int not null,
   timestamp float not null,
   checksum text not null);
create unique index checksum_cache_pk on checksum_cache(dev, ino);

create table run(
   run_name text not null,
   archive_dir text not null,
   is_complete int not null);
create unique index completed_run_pk on run(run_name);

