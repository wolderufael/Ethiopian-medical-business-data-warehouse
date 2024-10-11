{{ config(materialized='table') }}

SELECT *
FROM public.scrapped_data_cleaned