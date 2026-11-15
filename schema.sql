-- Run this once in Supabase > SQL Editor
create table messages (
  id bigint generated always as identity primary key,
  name text, email text, message text,
  created_at timestamptz default now()
);
create table counter (id int primary key, visits bigint not null default 0);
insert into counter values (1, 0);
create function increment_visits() returns bigint
language sql security definer as
$$ update counter set visits = visits + 1 where id = 1 returning visits; $$;
alter table messages enable row level security;
alter table counter enable row level security;
