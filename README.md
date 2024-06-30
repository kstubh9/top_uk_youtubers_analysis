# Top UK Youtubers Analysis
<img width="574" alt="image" src="https://github.com/kstubh9/top_uk_youtubers_analysis/assets/82211890/1447c409-bc86-425c-81cb-321198c10ce9">

## Objective
- What is the key pain point: 
The Head of Marketing is looking to identify the leading YouTubers of 2024 to determine the best candidates for running marketing campaigns for the remainder of the year.

- What is the ideal solution?
To create a dashboard that provides insights into the top UK YouTubers in 2024, it should include their:
- subscriber count
- total views
- total videos, and
- engagement metrics

This will assist the marketing team in making well-informed decisions about which YouTubers to partner with for their marketing campaigns.

## User Story
As the Head of Marketing, I need a dashboard to analyze YouTube channel data in the UK.

This dashboard should help me identify the top-performing channels based on metrics like subscriber count and average views.

Using this information, I can make better decisions about which YouTubers to partner with, ensuring each marketing campaign is as effective as possible.

## Data Source
We need data on the top UK YouTubers in 2024 that includes their:
- channel names
- total subscribers
- total views
- total videos uploaded

The dataset is sourced from [Kaggle](https://www.kaggle.com/datasets/bhavyadhingra00020/top-100-social-media-influencers-2024-countrywise?resource=download).
This dataset is not clean and does not contain all the fields required, therefore I developed a python script that uses [YouTube Data API v3](https://console.cloud.google.com/marketplace/product/google/youtube.googleapis.com?q=search&referrer=search&project=wise-sorter-428006-q0&supportedpurview=project)
to fetch data like total subscribers, total views, channel names and total videos uploaded.

## Content requirements of dashboard
To determine what the dashboard should include, we need to identify the key questions it needs to answer:

1. Who are the top 10 YouTubers with the most subscribers?
2. Which 3 channels have uploaded the most videos?
3. Which 3 channels have the highest total views?
4. Which 3 channels have the highest average views per video?
5. Which 3 channels have the highest views per subscriber ratio?
6. Which 3 channels have the highest subscriber engagement rate per video uploaded?

## Key Responsibilities
1. Get the data
2. Explore the data in Excel
3. Load the data into SQL Server
4. Clean the data with SQL
5. Test the data with SQL
6. Visualize the data in Power BI
7. Generate the findings based on the insights
8. Write the documentation 

## Tools and Technologies
| Tool	| Purpose |
|-------|---------|
| Excel	| Exploring the data |
| SQL Server |	Cleaning, testing, and analyzing the data |
| Python | Developing the script |
| Power BI | Visualizing the data via interactive dashboards |
| GitHub | Hosting the project documentation and version control |

## Analysis
### SQL Queries
1. Cleaning and Transformation

```sql
CREATE VIEW views_top_uk_youtubers AS
SELECT 
	CAST(SUBSTRING(NOMBRE, 1, (CHARINDEX('@', NOMBRE)-1))as VARCHAR(100)) as channel_name, 
	subscribers, 
	CAST(views AS BIGINT) as views, 
	videos 
FROM 
	updated_dataset
```

2. Data quality checks

```sql
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

```
### DAX Measures
Below are the DAX measures used in the report.

1. Average Views per Video (in Millions)
```dax
Average Views per Video (M) = 
VAR million = 1000000
VAR avgViewsPerVideo = DIVIDE(SUM(views_top_uk_youtubers[views]), SUM(views_top_uk_youtubers[videos]), BLANK())
VAR avgViewsinMill = DIVIDE(avgViewsPerVideo, million, BLANK())  
RETURN avgViewsinMill

```
2. Subscriber Engagement Rate
```dax
Subscriber Engagement Rate = 
VAR totalSubs = SUM(views_top_uk_youtubers[subscribers])
VAR totalVideos = SUM(views_top_uk_youtubers[videos])
VAR subEngRate = DIVIDE(totalSubs, totalVideos, BLANK())
RETURN subEngRate

```
3. Total Subscribers (in Millions)
```dax
Total Subscribers (M) = 
VAR million = 1000000
VAR sumOfTotalSubscribers = SUM(views_top_uk_youtubers[subscribers])
VAR totalSubscribers = DIVIDE(sumOfTotalSubscribers, million)
RETURN totalSubscribers

```
4. Total Videos 
```dax
Total Videos = 
VAR totalVideos = SUM(views_top_uk_youtubers[videos])
RETURN totalVideos

```
5. Total Views (in Billions)
```dax
Total Views (B) = 
VAR billion = 1000000000
VAR sumOfTotalViews = SUM(views_top_uk_youtubers[views])
VAR totalViews = DIVIDE(sumOfTotalViews, billion)
RETURN totalViews

```

6. Views Per Subscriber
```dax
Views Per Subscriber = 
VAR sumOfTotalViews = SUM(views_top_uk_youtubers[views])
VAR sumOfTotalSubscribers = SUM(views_top_uk_youtubers[subscribers])
VAR viewsPerSub = DIVIDE(sumOfTotalViews, sumOfTotalSubscribers, BLANK())
RETURN viewsPerSub
```

## Validation
### SQL Query

```sql
-- 1. Define variables.
DECLARE @conversionRate FLOAT = 0.02;		-- The conversion rate @ 2%
DECLARE @productCost FLOAT = 5.0;			-- The product cost @ $5
DECLARE @campaignCost FLOAT = 50000.0;		-- The campaign cost @ $50,000	


-- 2. Create a CTE to round the average views per video.
WITH ChannelData AS (
    SELECT 
        channel_name,
        views,
        videos,
        ROUND((CAST(views AS FLOAT) / videos), -4) AS rounded_avg_views_per_video
    FROM 
        views_top_uk_youtubers
)

-- 3. Select the necessary columns, create calculated columns from the existing ones.
SELECT 
    channel_name,
    rounded_avg_views_per_video,
    (rounded_avg_views_per_video * @conversionRate) AS potential_units_sold_per_video,
    (rounded_avg_views_per_video * @conversionRate * @productCost) AS potential_revenue_per_video,
    ((rounded_avg_views_per_video * @conversionRate * @productCost) - @campaignCost) AS net_profit
FROM 
    ChannelData


-- 4. Filter the results by YouTube channels.
WHERE 
    channel_name in ('NoCopyrightSounds', 'DanTDM', 'Dan Rhodes')    


-- 5. Sort the results by net profits in descending order. 
ORDER BY
	net_profit DESC

```

## Results
### Visualization

<img width="574" alt="Page 1" src="https://github.com/kstubh9/top_uk_youtubers_analysis/assets/82211890/de6b33a7-5f57-4b73-9111-1c7dd3dd710b">

### Insights
 
![image](https://github.com/kstubh9/top_uk_youtubers_analysis/assets/82211890/c4e2b3b0-fc5f-416e-a16e-e301f961a287)

### Validation (SQL)

![image](https://github.com/kstubh9/top_uk_youtubers_analysis/assets/82211890/da367040-712e-45f6-9a56-aff8e2db7de6)

**I performed calculations in Excel and validated the results using SQL. Both methods produced the same results.**

## Recommendations

-	Based on average views per subscriber and average views per video, **Dan Rhodes** appears to be the most viable option to invest in for most return, approximately **US$ 1,074,000.00**. 
-	Although the likes of **24 News HD, Sky News and BBC News** have a higher number of videos published, they are news channels with lower engagement rate and average views per video. Therefore **YOGSCAST Lewis and Simon, GRM Daily and Man City** are the channels with most number of videos along with higher channel statistics.  
-	However, it might be worth considering whether collaborating with them under the current budget constraints is worthwhile, given that the potential return on investment is significantly lower compared to other channels.
-	**Mister Max** is also a strong contender to invest in being one of the most subscribed channels and its videos averaging **14.04 million views.**
-	The top 3 channels to form collaborations with are **NoCopyrightSounds, DanTDM and Dan Rhodes** based on this analysis, because they attract the most engagement on their channels consistently.
 
## Key Achievements

- Successfully identified and analyzed top 3 Youtube channels to partner with.
- Developed and presented actionable insights and recommendations to the Head of Marketing, enabling informed decision-making to improve ROI.
- Enhanced data analysis and visualization skills, providing clear and impactful business insights through interactive dashboards.

This project demonstrates a strong ability to handle end-to-end data analysis tasks, from data extraction and transformation to insightful reporting and actionable recommendations, showcasing proficiency in SQL, Power BI, Python and DAX.



