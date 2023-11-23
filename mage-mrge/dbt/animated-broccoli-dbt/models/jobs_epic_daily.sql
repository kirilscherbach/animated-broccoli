{{
  config(
    materialized='incremental',
    unique_key='daily_job_id',
    description='This table contains a single open position from Epic registered as open per day and can be used for further analysis',
    alias='jobs_epic_daily',
    indexes=[
      {'columns': ['job_id', 'insert_date'], 'type': 'btree', 'unique': True},
      {'columns': ['insert_ts'], 'type': 'btree'},
    ]
  )
}}

select
    daily_job_id
    , absolute_url
    , title
    , department
    , company
    , remote
    , updated_at
    , insert_ts
    , insert_date
    , internal_job_id || requisition_id as job_id
    , city || ', ' || state || ', ' || country as job_location
from
    (
        select
            absolute_url
            , internal_job_id
            , requisition_id
            , title
            , department
            , company
            , remote
            , spotlight
            , city
            , state
            , country
            , updated_at
            , insert_ts
            , insert_ts::date as insert_date
            , concat(internal_job_id, '-', requisition_id, '-', insert_ts::date) as daily_job_id
            , row_number() over (partition by concat(internal_job_id, '-', requisition_id, '-', insert_ts::date) order by insert_ts desc) as rn
        from {{ source('scraper_results', 'jobs_epic') }}
        {% if is_incremental() %}
        -- this filter will only be applied on an incremental run
        -- (uses > to include records whose timestamp occurred since the last run of this model)
            where insert_ts > (select max(insert_ts) from {{ this }})
        {% endif %}
    ) as ordered_incr
where rn = 1
