create materialized view github as
select c.*, f.path, f.id from commits c
join files f on f.path = c.old_path or f.path = c.new_path;
