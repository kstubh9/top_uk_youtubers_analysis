CREATE VIEW views_top_uk_youtubers AS
SELECT 
	CAST(SUBSTRING(NOMBRE, 1, (CHARINDEX('@', NOMBRE)-1))as VARCHAR(100)) as channel_name, 
	subscribers, 
	CAST(views AS BIGINT) as views, 
	videos 
FROM 
	updated_dataset
