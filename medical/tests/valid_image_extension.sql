--  test to check the file extention of the files in Media Path 
SELECT *
FROM {{ ref('medical_data_transformed') }}  
WHERE LOWER("Media Path") NOT LIKE '%.jpg'
  AND LOWER("Media Path") NOT LIKE '%.jpeg'
  AND LOWER("Media Path") NOT LIKE '%.png'
