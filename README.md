# Kenya YouTube Channel Analysis

This project analyzes YouTube channels in Kenya using the YouTube Data API v3. It provides insights into video content, subscriber trends, and engagement metrics for Kenyan YouTube channels.

## Features

- Search for Kenyan YouTube channels
- Analyze channel statistics (subscribers, views, video count)
- Calculate average views for recent videos
- Generate visualizations:
  - Subscriber distribution
  - Correlation between total views and video count
  - Top 10 channels by subscribers

## Requirements

- Python 3.7+
- Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 Client ID (Desktop app)

## Installation

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```
   pip install google-auth-oauthlib google-api-python-client pandas matplotlib seaborn python-dotenv
   ```

3. Set up Google Cloud project and obtain the OAuth 2.0 Client ID:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project 
   - Enable the YouTube Data API v3
   - Create credentials (OAuth 2.0 Client ID) for a Desktop app
   - Download the client configuration and save it as `client_secret.json` in the project directory

## Usage

1. Run the main script:
   ```
   python kenya_youtube_analysis.py
   ```

2. Follow the authentication flow in your browser to grant the necessary permissions.

3. The script will search for Kenyan YouTube channels, analyze their data, and generate visualizations.

4. Output files:
   - `subscriber_distribution.png`: Histogram of subscriber counts
   - `views_vs_videos.png`: Scatter plot of total views vs. video count
   - `top_10_channels.png`: Bar chart of top 10 channels by subscribers


## Disclaimer

This project is for educational purposes only. 