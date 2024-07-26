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

### Workflow:

1. **Setup MySQL Database Connection**:
    - Establish a connection to the MySQL database using the provided credentials.
    - Create a cursor object to execute SQL queries.

2. **Fetch and Display Existing Comment Data**:
    - Query the `comment_data_two` table to retrieve all existing comments.
    - Convert the results into a Pandas DataFrame and display it.

3. **YouTube API Connection**:
    - Define a function to connect to the YouTube Data API using an API key.

4. **Retrieve Channel Details**:
    - Define a function to fetch channel details using the YouTube Data API.
    - Parse the response to extract relevant information.

5. **Create and Populate Channel Details Table**:
    - Create the `Channel_Five` table if it does not already exist.
    - Insert the fetched channel details into the `Channel_Five` table.

6. **Fetch and Display Channel Details**:
    - Query the `Channel_Five` table to retrieve all channel details.
    - Convert the results into a Pandas DataFrame and display it.

### Detailed Steps:

1. **Setup MySQL Database Connection**:

```python
import mysql.connector
import pandas as pd

# Establish MySQL database connection
client = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1611',
    database='YoutubeDataHarvesting'
)

# Create a cursor object to execute SQL queries
cursor = client.cursor()
```

2. **Fetch and Display Existing Comment Data**:

```python
# Query to select all data from comment_data_two table
query = "SELECT * FROM comment_data_two"

# Execute the query
cursor.execute(query)

# Fetch all the results
result = cursor.fetchall()

# Define column names
columns = [col[0] for col in cursor.description]

# Create DataFrame
df = pd.DataFrame(result, columns=columns)

# Display DataFrame
print(df)
```

3. **YouTube API Connection**:

```python
import mysql.connector
from googleapiclient.discovery import build
import pandas as pd

# Define the global youtube object
youtube = None

def api_connect():
    global youtube  # Define youtube as global
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "YOUR_API_KEY"  # Replace this with your actual API key

    youtube = build(api_service_name, api_version, developerKey=api_key)
    return youtube
```

4. **Retrieve Channel Details**:

```python
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    result = request.execute()
    
    data = []
    if 'items' in result:
        for item in result['items']:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            data.append({
                'Channel_Name': snippet.get('title', 'Unknown Title'),
                'Channel_ID': item['id'],
                'Channel_Description': snippet.get('description', 'No description available'),
                'PlayListID': item['contentDetails'].get('relatedPlaylists', {}).get('uploads', 'Unknown Playlist'),
                'PublishedAt': snippet.get('publishedAt', 'No YearOfPublishing'),
                'ViewCount': statistics.get('viewCount', 0),
                'VideoCount': statistics.get('videoCount', 0),
                'SubscriberCount': statistics.get('subscriberCount', 0)
            })
    else:
        print("No items found in the response.")
        
    return data
```

5. **Create and Populate Channel Details Table**:

```python
# Create Channel_Five table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS Channel_Five (Channel_ID VARCHAR(100) PRIMARY KEY, Channel_Name VARCHAR(300), Channel_Description TEXT, PlayListID TEXT, ViewCount INT, VideoCount INT, SubscriberCount INT, PublishedAt DATETIME)")

# Define channel IDs
channel_ids = ['UCH86ITmgOsa8amIFhGCgcTQ', 'UCOrQAdzm-lwk-Pj_e6vKQjg', 'UCymeXH2TJW58p5WcSeyDc3g', 'UCr1tgA4LWxttjEOR_ySEzDA', 'UCgsyJ5oeftrhdnpUIqsfexw', 'UCw3rlo-az-90uz66bFgU3uw', 'UCYHfntv8p9G4c5ihe2NQM2w', 'UCrPUWWNTzeY2uJ96xUuyn0g', 'UCud4Bh-uxJz1Hu4ZWo76J6Q', 'UC8N84h1aPhwI5IT8jPh_u9Q']

# Iterate through channel IDs
for channel_id in channel_ids:
    channel_id = str(channel_id)
    youtube = api_connect()
    channel_details = get_channel_details(channel_id)

    if channel_details:  # Check if channel_details is not empty
        for channel_detail in channel_details:
            try:
                # Insert channel details into the database
                query = "INSERT IGNORE INTO Channel_Five (Channel_ID, Channel_Name, Channel_Description, PlayListID, ViewCount, VideoCount, SubscriberCount, PublishedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (channel_detail['Channel_ID'], channel_detail['Channel_Name'], channel_detail['Channel_Description'], channel_detail['PlayListID'], channel_detail['ViewCount'], channel_detail['VideoCount'], channel_detail['SubscriberCount'], channel_detail['PublishedAt']))
                client.commit()
            except mysql.connector.Error as err:
                print(f"Error inserting channel details: {err}")
```

6. **Fetch and Display Channel Details**:

```python
# Fetch data from the database
query = 'SELECT * FROM Channel_Five'
cursor.execute(query)
result = cursor.fetchall()

# Define column names
columns = ['Channel_ID', 'Channel_Name', 'Channel_Description', 'PlayListID', 'ViewCount', 'VideoCount', 'SubscriberCount', 'PublishedAt']

# Create DataFrame
df = pd.DataFrame(result, columns=columns)

# Display DataFrame
print(df)
```

### Execution:

1. **Install Required Packages**:
    - Ensure you have `mysql-connector-python`, `google-api-python-client`, and `pandas` installed.
    ```bash
    pip install mysql-connector-python google-api-python-client pandas
    ```

2. **Run the Script**:
    - Execute the Python script to establish the database connection, fetch video and comment data, store it in the MySQL database, and display the results.

### Notes:
- Replace `"YOUR_API_KEY"` with your actual YouTube API key.
- Ensure the MySQL database credentials (host, user, password, database) are correct.

###Workflow:

1. **Setup Database Connection**:
    - Establish a connection to the MySQL database.
    - Create a cursor object to execute SQL queries.
    - Ensure that the `Duration` column in the `Video_Data_One` table has sufficient length.

2. **Define Functions for YouTube API Interaction**:
    - `get_all_video_ids(c_id)`: Retrieve all video IDs from a given YouTube channel's uploads playlist.
    - `get_video_details(v_id)`: Fetch details of a specific video using its ID.

3. **Create Video Data Table**:
    - Create the `Video_Data_One` table if it does not already exist.

4. **Fetch and Store Video Details**:
    - Iterate through a list of channel IDs, fetching video IDs for each channel.
    - Retrieve and store details of each video in the database, updating existing entries or inserting new ones.

5. **Convert Duration Format**:
    - Convert ISO 8601 duration strings to total seconds and update the database.

6. **Fetch and Display Updated Data**:
    - Query the database to fetch updated video data.
    - Convert the result into a Pandas DataFrame and display it.

7. **Close Database Connection**:
    - Close the cursor and database connection.

### Detailed Steps:

1. **Setup Database Connection**:

```python
import mysql.connector

# Establish database connection
client = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1611',
    database='YoutubeDataHarvesting'
)
cursor = client.cursor()

# Ensure Duration column has sufficient length
cursor.execute("ALTER TABLE Video_Data_One MODIFY COLUMN Duration VARCHAR(255)")
```

2. **Define Functions for YouTube API Interaction**:

```python
from googleapiclient.discovery import build
from isodate import parse_duration, ISO8601Error

def get_all_video_ids(c_id):
    youtube = build("youtube", "v3", developerKey="YOUR_API_KEY")
    request = youtube.channels().list(
        part="contentDetails,statistics",
        id=c_id
    )
    response = request.execute()
    
    try:
        p_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Retrieve video IDs from playlist
        v_ids = []
        next_page_token = None
        while True:
            playlist_items_request = youtube.playlistItems().list(
                part="snippet",
                playlistId=p_id,
                pageToken=next_page_token
            )
            playlist_items_response = playlist_items_request.execute()

            for item in playlist_items_response["items"]:
                v_ids.append(item["snippet"]["resourceId"]["videoId"])

            next_page_token = playlist_items_response.get("nextPageToken")
            if not next_page_token:
                break

        return v_ids
    except KeyError:
        print(f"No 'items' key found in the response for channel ID: {c_id}")
        return []

def get_video_details(v_id):
    youtube = build("youtube", "v3", developerKey="YOUR_API_KEY")
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=v_id
    )
    response = request.execute()
    
    video_data = []
    if 'items' in response:
        for item in response['items']:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            video_data.append({
                'Video_Name': snippet.get('title', 'Unknown Title'),
                'Channel_ID': snippet.get('channelId', 'Unknown Channel_ID'),
                'Duration': item['contentDetails'].get('duration', 'Unknown Duration'),
                'ViewCount': statistics.get('viewCount', 0),
                'LikeCount': statistics.get('likeCount', 0),
                'DisLikeCount': statistics.get('dislikeCount', 0),
                'CommentCount': statistics.get('commentCount', 0)
            })
    else:
        print('No items found in the response.')
    return video_data
```

3. **Create Video Data Table**:

```python
# Create Video_Data_One table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS Video_Data_One (Video_Name VARCHAR(300), Channel_ID VARCHAR(100), Duration VARCHAR(255), ViewCount INT, LikeCount INT, DisLikeCount INT, CommentCount INT)")
```

4. **Fetch and Store Video Details**:

```python
# Example usage
channel_ids = ['UCOrQAdzm-lwk-Pj_e6vKQjg', 'UCymeXH2TJW58p5WcSeyDc3g', 'UCr1tgA4LWxttjEOR_ySEzDA', 'UCgsyJ5oeftrhdnpUIqsfexw', 'UCH86ITmgOsa8amIFhGCgcTQ', 'UCYHfntv8p9G4c5ihe2NQM2w', 'UCrPUWWNTzeY2uJ96xUuyn0g', 'UCud4Bh-uxJz1Hu4ZWo76J6Q', 'UC8N84h1aPhwI5IT8jPh_u9Q', 'UCJl5FQGoF1PRivoGecGJNuA']

for c_id in channel_ids:
    c_id = str(c_id)
    video_ids = get_all_video_ids(c_id)
   
    for video_id in video_ids:
        video_id = str(video_id)
        video_details = get_video_details(video_id)

        for detail in video_details:
            video_name = detail['Video_Name']

            # Check if the video already exists in the database
            cursor.execute("SELECT COUNT(*) FROM Video_Data_One WHERE Video_Name = %s", (video_name,))
            count = cursor.fetchone()[0]

            if count > 0:
                # If the video already exists, update its data
                update_query = "UPDATE Video_Data_One SET Channel_ID = %s, Duration = %s, ViewCount = %s, LikeCount = %s, DisLikeCount = %s, CommentCount = %s WHERE Video_Name = %s"
                cursor.execute(update_query, (detail['Channel_ID'], detail['Duration'], detail['ViewCount'], detail['LikeCount'], detail['DisLikeCount'], detail['CommentCount'], video_name))
            else:
                # If the video doesn't exist, insert a new entry
                insert_query = "INSERT INTO Video_Data_One (Video_Name, Channel_ID, Duration, ViewCount, LikeCount, DisLikeCount, CommentCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (detail['Video_Name'], detail['Channel_ID'], detail['Duration'], detail['ViewCount'], detail['LikeCount'], detail['DisLikeCount'], detail['CommentCount']))
            
            client.commit()  # Commit the changes
```

5. **Convert Duration Format**:

```python
# Fetch the data and convert the ISO 8601 durations to seconds
def convert_duration_to_seconds(duration):
    if isinstance(duration, str):
        try:
            return int(parse_duration(duration).total_seconds())
        except ISO8601Error:
            print(f"Unable to parse duration: {duration}")
            return None
    else:
        # If the duration is already a number, return it as is
        return duration

cursor.execute("SELECT Video_Name, Duration FROM Video_Data_One")
rows = cursor.fetchall()

for row in rows:
    video_name, iso_duration = row
    duration_seconds = convert_duration_to_seconds(iso_duration)
    
    if duration_seconds is not None:
        cursor.execute("""
            UPDATE Video_Data_One 
            SET Duration = %s 
            WHERE Video_Name = %s
        """, (duration_seconds, video_name))
        client.commit()
```

6. **Fetch and Display Updated Data**:

```python
# Fetch the updated data from the database to verify the changes
query = 'SELECT * FROM Video_Data_One'
cursor.execute(query)
result = cursor.fetchall()
df = pd.DataFrame(result, columns=[
    'Video_Name', 'Channel_ID', 'Duration', 'ViewCount', 'LikeCount', 'DisLikeCount', 'CommentCount'
])

# Print the DataFrame
print(df)
```

7. **Close Database Connection**:

```python
# Close the cursor and database connection
cursor.close()
client.close()
```

### Execution:

1. **Install Required Packages**:
    - Ensure you have `mysql-connector-python`, `google-api-python-client`, `pandas`, and `isodate` installed.
    ```bash
    pip install mysql-connector-python google-api-python-client pandas isodate
    ```

2. **Run the Script**:
    - Execute the Python script to establish the database connection, fetch video data, store it in the MySQL database, and display the results.

### Notes:
- Replace `"YOUR_API_KEY"` with your actual YouTube API key.
- Ensure the MySQL database credentials (host, user, password, database) are correct.
