{{ config(materialized='table') }}

WITH filtered_medical_data AS (
    SELECT *
    FROM {{ source('public', 'scrapped_data_cleaned') }}
    WHERE "Media Path" !='No Media'
    AND "Channel Username" IN ('@CheMed123','@lobelia4cosmetics')
)

SELECT
    "Channel Title",
    "Channel Username",
    "Message",
    "Date",
    "Media Path"
FROM filtered_medical_data
