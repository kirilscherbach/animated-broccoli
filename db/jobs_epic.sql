drop table if exists public.jobs_epic;
create table public.jobs_epic (
    id SERIAL primary key,
    absolute_url TEXT,
    education TEXT,
    internal_job_id TEXT,
    requisition_id TEXT,
    title TEXT,
    content TEXT,
    department TEXT,
    company TEXT,
    remote TEXT,
    spotlight TEXT,
    type TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    filtertext TEXT,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    full_response JSONB,
    insert_ts TIMESTAMP WITHOUT TIME ZONE
);

create index insert_ts_btree_epic on jobs_epic using btree
(
    insert_ts
);

grant all on public.jobs_epic to scraper;
grant all on public.jobs_epic to dbt_user;
grant all on sequence jobs_epic_new_id_seq to scraper;
