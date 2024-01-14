drop table if exists public.jobs_crytek;
create table public.jobs_crytek (
    id SERIAL primary key,
    job_id TEXT,
    additional_plain TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    description_plain TEXT,
    lists JSONB,
    job_title TEXT,
    hosted_url TEXT,
    apply_url TEXT,
    commitment TEXT,
    department TEXT,
    job_location TEXT,
    team TEXT,
    date_posted DATE,
    valid_through DATE,
    full_response JSONB,
    insert_ts TIMESTAMP WITHOUT TIME ZONE
);

create index insert_ts_btree_crytek on jobs_crytek using btree
(
    insert_ts
);

grant all on sequence jobs_crytek_new_id_seq to scraper;
