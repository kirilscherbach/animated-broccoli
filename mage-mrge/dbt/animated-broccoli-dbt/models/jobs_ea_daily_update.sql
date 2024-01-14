{{
  config(
    materialized='incremental',
    unique_key='update_job_id',
    description='This table contains summary of added or removed positions from EA',
    alias='jobs_ea_daily_update',
    indexes=[
      {'columns': ['insert_date'], 'type': 'btree'},
    ],
  )
}}

{{ calculate_daily_job_update('jobs_ea_clean', 'Electronic Arts') }}
