{{
  config(
    materialized='incremental',
    unique_key='update_job_id',
    description='This table contains summary of added or removed positions from Chymera',
    alias='jobs_chymera_daily_update',
    indexes=[
      {'columns': ['insert_date'], 'type': 'btree'},
    ],
  )
}}

{{ calculate_daily_job_update('jobs_chymera_clean', 'Chymera') }}
