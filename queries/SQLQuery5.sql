/*

Data Quality checks
1. row count should be equal to 100
2. check for data types
3. column count should be equal to 4
4. check for duplicates

*/

-- 1. row count should be equal to 4
SELECT 
	COUNT(*) as row_count
FROM 
	views_top_uk_youtubers

-- 2. check for data types

SELECT 
	COLUMN_NAME, DATA_TYPE 
FROM 
	INFORMATION_SCHEMA.COLUMNS 
WHERE	
	TABLE_NAME = 'views_top_uk_youtubers'

-- column count should be equal to 4

SELECT 
	COUNT(*) AS coumn_count
FROM 
	INFORMATION_SCHEMA.COLUMNS
WHERE
	TABLE_NAME = 'views_top_uk_youtubers'

-- 4. check for duplicates

SELECT 
	channel_name, COUNT(*) AS duplicate_count
FROM 
	views_top_uk_youtubers
GROUP BY 
	channel_name 
HAVING 
	COUNT(*) > 1
