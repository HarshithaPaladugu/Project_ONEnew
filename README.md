# Project_ONEnew

### Workflow:

1. **Setup Database Connection**:
    - Establish a connection to the MySQL database using the provided credentials.
    - Ensure the database `YoutubeDataHarvesting` and the table `comment_data_two` exist.

2. **Retrieve Video IDs**:
    - Use the YouTube Data API to get the list of video IDs from the specified channels.

3. **Fetch Comments for Each Video**:
    - For each video ID, check if comments are enabled.
    - Retrieve comments for each video and format the necessary details.

4. **Store Comments in the Database**:
    - Insert the fetched comments into the MySQL table `comment_data_two`.

5. **Error Handling**:
    - Include error handling for network issues, API limits, and data inconsistencies.

### Detailed Steps:

1. **Setup MySQL Database Connection**:

```python
import mysql.connector
import googleapiclient.discovery
import re

# Connect to MySQL database
client = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1611',
    database='YoutubeDataHarvesting'
)

cursor = client.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS comment_data_two (
    commentID VARCHAR(255) PRIMARY KEY,
    videoID VARCHAR(255),
    textdisplay TEXT,
    authordisplayname VARCHAR(255),
    publishedAt DATETIME
)
""")
```

2. **Fetch Video IDs from YouTube Channel**:

```python
def get_all_video_ids(c_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUR_API_KEY")
    request = youtube.channels().list(
        part="contentDetails",
        id=c_id
    )
    try:
        response = request.execute()
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        video_ids = []
        next_page_token = None
        while True:
            playlist_items_request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                pageToken=next_page_token
            )
            playlist_items_response = playlist_items_request.execute()

            for item in playlist_items_response.get("items", []):
                video_ids.append(item["snippet"]["resourceId"]["videoId"])

            next_page_token = playlist_items_response.get("nextPageToken")
            if not next_page_token:
                break

        return video_ids
    except KeyError as e:
        print(f"KeyError: {e}")
        return []
    except Exception as e:
        print(f"Error fetching video IDs for channel {c_id}: {e}")
        return []
```

3. **Fetch Comments for Each Video**:

```python
def get_comments(video_ids, api_key, max_comments=100):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    comments = []

    for video_id in video_ids:
        try:
            # Check if comments are disabled for the video
            video_request = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            video_response = video_request.execute()
            comment_count = int(video_response["items"][0]["statistics"]["commentCount"])
            if comment_count == 0:
                print(f"Comments are disabled for the video: {video_id}")
                continue

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_comments
            )
            response = request.execute()

            for item in response["items"]:
                comment_info = {
                    "commentID": item["snippet"]["topLevelComment"]["id"],
                    "videoID": video_id,
                    "textdisplay": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    "authordisplayname": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    "publishedAt": re.sub(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})Z', r'\1 \2', item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
                }

                # Insert comment into MySQL table
                insert_query = "INSERT INTO comment_data_two (commentID, videoID, textdisplay, authordisplayname, publishedAt) VALUES (%s, %s, %s, %s, %s)"
                insert_values = (comment_info["commentID"], comment_info["videoID"], comment_info["textdisplay"], comment_info["authordisplayname"], comment_info["publishedAt"])
                cursor.execute(insert_query, insert_values)
                client.commit()

                comments.append(comment_info)

        except Exception as e:
            print(f"Error fetching comments for {video_id}: {e}")

    return comments
```

4. **Main Execution Loop**:

```python
channel_ids = ['UCJl5FQGoF1PRivoGecGJNuA', 'UCOrQAdzm-lwk-Pj_e6vKQjg', 'UCymeXH2TJW58p5WcSeyDc3g', 'UCr1tgA4LWxttjEOR_ySEzDA', 'UCgsyJ5oeftrhdnpUIqsfexw', 'UCH86ITmgOsa8amIFhGCgcTQ', 'UCYHfntv8p9G4c5ihe2NQM2w', 'UCrPUWWNTzeY2uJ96xUuyn0g', 'UCud4Bh-uxJz1Hu4ZWo76J6Q', 'UC8N84h1aPhwI5IT8jPh_u9Q']

for c_id in channel_ids:
    video_ids = get_all_video_ids(c_id)
    api_key = "YOUR_API_KEY"
    comments_details = get_comments(video_ids, api_key)
    print(comments_details)
```

### Notes:

- **API Key**: Replace `"YOUR_API_KEY"` with your actual YouTube API key.
- **Database Credentials**: Ensure the database credentials (host, user, password) are correct.
- **Error Handling**: Add more specific error handling as needed for production.

This structure ensures that the code is modular, easy to maintain, and ready for execution. Let me know if you need any further help!
