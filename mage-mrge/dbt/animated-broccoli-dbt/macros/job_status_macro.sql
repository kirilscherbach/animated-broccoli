{% macro calculate_daily_job_update(table_name) %}


with filtered_dataset as (select * from
(select
        *
        , dense_rank() over (order by insert_date desc) as position
    from {{ ref(table_name) }}
    where
    insert_date between '{{ var("execution_date", "2023-11-02") }}'::date - 7
                    and '{{ var("execution_date", "2023-11-02") }}'::date
)
where position <= 2
)

/*
today                   yesterday
insert_date position    insert_date position
2022-01-05  1           2022-01-05  0
2022-01-03  2           2022-01-03  1
2022-01-02  3           2022-01-02  2
*/

select
  coalesce(today.job_id, yesterday.job_id)||'{{ var("execution_date", "2023-11-02") }}' update_job_id
  , case
        when today.job_id is null then 'Position closed'
        when yesterday.job_id is null then 'Position opened'
        else 'No change'
    end as job_status
, coalesce(today.job_id, yesterday.job_id) as job_id
, coalesce(today.absolute_url, yesterday.absolute_url) as absolute_url
, coalesce(today.title , yesterday.title ) as title
, coalesce(today.department , yesterday.department ) as department
, coalesce(today.company , yesterday.company ) as company
, coalesce(today.remote , yesterday.remote ) as remote
, coalesce(today.job_location , yesterday.job_location ) as job_location
, '{{ var("execution_date", "2023-11-02") }}'::date as insert_date
from
filtered_dataset as today full outer join filtered_dataset as yesterday
on today.job_id = yesterday.job_id
and today.position = (yesterday.position-1)
where today.job_id is null or yesterday.job_id is null

{% endmacro %}
