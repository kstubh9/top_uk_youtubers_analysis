import pandas as pd
import re
from googleapiclient.discovery import build

# Function to extract channel name from the second column
def extract_channel_name(channel_info):
    return re.split(r' @', channel_info)[0]

# Function to get channel statistics using YouTube API
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    return stats['subscriberCount'], stats['viewCount'], stats['videoCount']

# Load the dataset
df = pd.read_csv('youtube_data_united-kingdom.csv')

# Extract channel name
df['channel_name'] = df.iloc[:, 1].apply(extract_channel_name)

# Initialize YouTube API
api_key = 'AIzaSyBiOvHbFsfULZ_wvz4UvW8L3LSTGRq-k00'
youtube = build('youtube', 'v3', developerKey=api_key)

# Extract channel ID and get channel stats
df['channel_id'] = df.iloc[:, 1].apply(lambda x: re.split(r' @', x)[1])
df['subscribers'] = 0
df['views'] = 0
df['videos'] = 0

for index, row in df.iterrows():
    try:
        subscribers, views, videos = get_channel_stats(youtube, row['channel_id'])
        df.at[index, 'subscribers'] = subscribers
        df.at[index, 'views'] = views
        df.at[index, 'videos'] = videos
    except Exception as e:
        print(f"An error occurred for channel {row['channel_name']}: {e}")

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_dataset.csv', index=False)
