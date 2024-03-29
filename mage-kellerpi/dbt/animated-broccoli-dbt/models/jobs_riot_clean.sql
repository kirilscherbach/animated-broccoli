{{
  config(
    materialized='incremental',
    unique_key='daily_job_id',
    description='This table contains a single open position from Riot registered as open per day and can be used for further analysis',
    alias='jobs_riot_clean',
    indexes=[
      {'columns': ['job_id', 'insert_date'], 'type': 'btree', 'unique': True},
      {'columns': ['insert_ts'], 'type': 'btree'},
    ]
  )
}}

select
    daily_job_id
    , absolute_url
    , job_id
    , title
    , department
    , company
    , remote
    , job_location
    , insert_ts
    , insert_date
from
    (
        select
            apply_url as absolute_url
            , job_id
            , title
            , department
            , company
            , job_location
            , insert_ts
            , insert_ts::date as insert_date
            , concat(job_id, '-', insert_ts::date) as daily_job_id
            , coalesce(lower(job_location) like '%remote%', 'false') as remote
            , row_number() over (partition by concat(job_id, '-', insert_ts::date) order by insert_ts desc) as rn
        from {{ source('scraper_results', 'jobs_riot') }}
        {% if is_incremental() %}
        -- this filter will only be applied on an incremental run
        -- (uses > to include records whose timestamp occurred since the last run of this model)
        where insert_ts > (select coalesce(max(insert_ts), '2020-01-01T00:00:00.000000') from {{ this }})
        {% endif %}
    ) as ordered_incr
where rn = 1
