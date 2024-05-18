import streamlit as st
import mysql.connector
import pandas as pd
from googleapiclient.discovery import build

# Initialize YouTube API connection
youtube = None

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1611',
        database='YoutubeDataHarvesting'
    )

# Function to get channel details from YouTube API
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

# Function to connect to YouTube API
def api_connect():
    global youtube  # Define youtube as global
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyB6F26A1bBXkTNjLIQm8DEAQs8e6R2xbYk"  # Replace this with your actual API key

    youtube = build(api_service_name, api_version, developerKey=api_key)

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://www.caspio.com/wp-content/uploads/blog/what-you-need-to-know-about-data-harvesting-and-how-to-prevent-it.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stApp * {
            color: black;  /* Change text color to black */
            font-size: 30px; /* Increase font size to 30px */
            font-weight: bold; /* Make text bold */
        }
        .stButton>button {
            background-color: skyblue; /* Change button color to sky blue */
            color: black; /* Change button text color to black */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Streamlit layout
    st.title("YouTube Data Harvesting")
    user_input = st.text_input("Enter YouTube Channel_ID")

    if st.button("Submit"):
        if user_input:
            channel_id = str(user_input)
            api_connect()
            channel_details = get_channel_details(channel_id)
            for channel_detail in channel_details:
                try:
                    query = """
                    INSERT IGNORE INTO Channel_Five (Channel_ID, Channel_Name, Channel_Description, PlayListID, ViewCount, VideoCount, SubscriberCount, PublishedAt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        channel_detail['Channel_ID'], channel_detail['Channel_Name'], channel_detail['Channel_Description'],
                        channel_detail['PlayListID'], channel_detail['ViewCount'], channel_detail['VideoCount'],
                        channel_detail['SubscriberCount'], channel_detail['PublishedAt']
                    ))
                    connection.commit()
                except mysql.connector.Error as err:
                    print(f"Error inserting channel details: {err}")

            # Execute the query based on user input
            query = f"SELECT Channel_Name, VideoCount, PlayListID, SubscriberCount FROM Channel_Five WHERE Channel_ID = '{user_input}'"
            cursor.execute(query)
            result = cursor.fetchone()  # Fetch a single row

            if result:
                # Create DataFrame from the fetched row
                df = pd.DataFrame([result], columns=['Channel_Name', 'VideoCount', 'PlayListID', 'SubscriberCount'])
                st.write("Channel Information:")
                st.write(df)
            else:
                st.write("No data found for the given Channel ID")

    # Query selection
    option = st.selectbox(
        'Select one of the following questions',
        (
            '1. What are the names of all the videos and their corresponding channels?', 
            '2. Which channels have the most number of videos, and how many videos do they have?', 
            '3. What are the top 10 most viewed videos and their respective channels?',
            '4. How many comments were made on each video, and what are their corresponding video names?',
            '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
            '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
            '7. What is the total number of views for each channel, and what are their corresponding channel names?',
            '8. What are the names of all the channels that have published videos in the year 2022?',
            '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
            '10. Which videos have the highest number of comments, and what are their corresponding channel names?'
        )
    )
    
    query = ""
    column_names = []

    if option.startswith('1.'):
        query = "SELECT Video_Data_One.Video_Name, Channel_Five.Channel_Name FROM Video_Data_One JOIN Channel_Five ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID"
        column_names = ['Video_Name', 'Channel_Name']
    elif option.startswith('2.'):
        query = "SELECT Channel_Name, VideoCount FROM Channel_Five ORDER BY VideoCount DESC LIMIT 5"
        column_names = ['Channel_Name', 'Video_Count']
    elif option.startswith('3.'):
        query = "SELECT Video_Data_One.Video_Name, Video_Data_One.ViewCount, Channel_Five.Channel_Name FROM Video_Data_One JOIN Channel_Five ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID ORDER BY Video_Data_One.ViewCount DESC LIMIT 10"
        column_names = ['Video_Name', 'ViewCount', 'Channel_Name']
    elif option.startswith('4.'):
        query = "SELECT Video_Name, CommentCount FROM Video_Data_One"
        column_names = ['Video_Name', 'CommentCount']
    elif option.startswith('5.'):
        query = """
        SELECT Video_Name, Video_Data_One.LikeCount, Channel_Five.Channel_Name 
        FROM Video_Data_One JOIN Channel_Five 
        ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID 
        WHERE Video_Data_One.LikeCount = (SELECT MAX(LikeCount) FROM Video_Data_One)
        """
        column_names = ['Video_Name', 'LikeCount', 'Channel_Name']
    elif option.startswith('6.'):
        query = "SELECT Video_Name, Video_Data_One.LikeCount, Video_Data_One.DisLikeCount FROM Video_Data_One"
        column_names = ['Video_Name', 'LikeCount', 'DisLikeCount']
    elif option.startswith('7.'):
        query = "SELECT Channel_Five.ViewCount, Channel_Name FROM Channel_Five"
        column_names = ['ViewCount', 'Channel_Name']
    elif option.startswith('8.'):
        query = "SELECT Channel_Five.Channel_Name, Channel_Five.PublishedAt FROM Channel_Five WHERE YEAR(Channel_Five.PublishedAt) = 2022"
        column_names = ['Channel_Name', 'PublishedAt']
    elif option.startswith('9.'):
        query = """
        SELECT Channel_Five.Channel_Name, AVG(Video_Data_One.Duration) AS Average_Duration_in_Seconds
        FROM Channel_Five JOIN Video_Data_One 
        ON Channel_Five.Channel_ID = Video_Data_One.Channel_ID 
        GROUP BY Channel_Five.Channel_Name
        """
        column_names = ['Channel_Name', 'Average_Duration_in_Seconds']
    elif option.startswith('10.'):
        query = """
        SELECT Video_Data_One.Video_Name, Video_Data_One.CommentCount, Channel_Five.Channel_Name 
        FROM Channel_Five JOIN Video_Data_One 
        ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID 
        WHERE Video_Data_One.CommentCount = (SELECT MAX(CommentCount) FROM Video_Data_One)
        """
        column_names = ['Video_Name', 'Comment_Count', 'Channel_Name']
    
    if st.button("Execute the Query"):
        if query:  # Check if query is not empty
            cursor.execute(query)
            result = cursor.fetchall()
        else:
            result = None  # Initialize result with None if query is empty

        # Display the result
        if result:
            df = pd.DataFrame(result, columns=column_names)
            st.write("Query Result:")
            st.write(df)
        else:
            st.write("No data found for the selected query")

    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
