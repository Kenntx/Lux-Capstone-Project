import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally. 
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Search for Kenyan YouTube channels
    kenyan_channels = search_kenyan_channels(youtube)

    # Analyze channels
    channel_data = analyze_channels(youtube, kenyan_channels)

    # Create visualizations
    create_visualizations(channel_data)

def search_kenyan_channels(youtube):
    channels = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            maxResults=50,
            q="Kenya",
            type="channel",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            channels.append(item['snippet']['channelId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return channels

def analyze_channels(youtube, channel_ids):
    channel_data = []

    for channel_id in channel_ids:
        try:
            # Get channel statistics
            channel_response = youtube.channels().list(
                part="snippet,statistics",
                id=channel_id
            ).execute()

            channel_info = channel_response['items'][0]
            
            # Get recent videos
            videos_response = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                type="video",
                order="date",
                maxResults=10
            ).execute()

            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            
            # Get video statistics
            video_stats_response = youtube.videos().list(
                part="statistics",
                id=','.join(video_ids)
            ).execute()

            avg_views = sum(int(video['statistics']['viewCount']) for video in video_stats_response['items']) / len(video_stats_response['items'])
            
            channel_data.append({
                'title': channel_info['snippet']['title'],
                'subscribers': int(channel_info['statistics']['subscriberCount']),
                'total_views': int(channel_info['statistics']['viewCount']),
                'video_count': int(channel_info['statistics']['videoCount']),
                'avg_recent_views': avg_views
            })

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            continue

    return pd.DataFrame(channel_data)

def create_visualizations(df):
    # Subscriber distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['subscribers'], kde=True)
    plt.title('Distribution of Subscribers for Kenyan YouTube Channels')
    plt.xlabel('Number of Subscribers')
    plt.ylabel('Count')
    plt.savefig('subscriber_distribution.png')
    plt.close()

    # Correlation between total views and video count
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='video_count', y='total_views')
    plt.title('Correlation between Total Views and Video Count')
    plt.xlabel('Number of Videos')
    plt.ylabel('Total Views')
    plt.savefig('views_vs_videos.png')
    plt.close()

    # Top 10 channels by subscribers
    top_10 = df.nlargest(10, 'subscribers')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10, x='title', y='subscribers')
    plt.title('Top 10 Kenyan YouTube Channels by Subscribers')
    plt.xlabel('Channel Title')
    plt.ylabel('Number of Subscribers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_10_channels.png')
    plt.close()

if __name__ == "__main__":
    main()