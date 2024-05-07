import streamlit as st
import mysql.connector
import pandas as pd
from googleapiclient.discovery import build
from isodate import parse_duration


# Database connection function
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1611',
        database='YoutubeDataHarvesting'
    )

# Streamlit app
def main():
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Streamlit layout
    st.title("YouTube Data Harvesting")
    user_input = st.selectbox( 'Select an option',
        ('UC8N84h1aPhwI5IT8jPh_u9Q',
                              'UCgsyJ5oeftrhdnpUIqsfexw',
                              'UCH86ITmgOsa8amIFhGCgcTQ',
                              'UCOrQAdzm-lwk-Pj_e6vKQjg',
                              'UCr1tgA4LWxttjEOR_ySEzDA',
                              'UCrPUWWNTzeY2uJ96xUuyn0g',
                              'UCud4Bh-uxJz1Hu4ZWo76J6Q',
                              'UCw3rlo-az-90uz66bFgU3uw',
                              'UCYHfntv8p9G4c5ihe2NQM2w',
                              'UCymeXH2TJW58p5WcSeyDc3g'))

    

    if st.button("Submit"):
        if user_input:
            # Execute the query based on user input
            query = f"SELECT Channel_Name, VideoCount, PlayListID, SubscriberCount FROM Channel_Five WHERE Channel_Five.Channel_ID = '{user_input}'"
            cursor.execute(query)
            result = cursor.fetchone()  # Fetch a single row

            if result:
                # Create DataFrame from the fetched row
                df = pd.DataFrame([result], columns=['Channel_Name', 'VideoCount', 'PlayListID', 'SubscriberCount'])
                st.write("Channel Information:")
                st.write(df)
            else:
                st.write("No data found for the given Channel ID")

    option = st.selectbox(
    'Select an option',
    ('1.What are the names of all the videos and their corresponding channels?', 
     '2.Which channels have the most number of videos, and how many videos do they have?', 
     '3.What are the top 10 most viewed videos and their respective channels?',
     '4.How many comments were made on each video, and what are their corresponding video names?',
     '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
     '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
     '7.What is the total number of views for each channel, and what are their corresponding channel names?',
     '8.What are the names of all the channels that have published videos in the year 2022?',
     '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
     '10.Which videos have the highest number of comments, and what are their corresponding channel names?'))
   
    query = ""
    
    if option.startswith('1.'):
        query = "SELECT Video_Data_One.Video_Name, Channel_Five.Channel_Name FROM Video_Data_One JOIN Channel_Five ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID"
        column_names=['Video_Name,Channel_name']
    elif option.startswith('2.'):
        query = "SELECT Channel_Name, VideoCount FROM Channel_Five ORDER BY VideoCount DESC LIMIT 5"
        column_names=['Channel_Name,Video_Count']
    elif option.startswith('3.'):
        query = "SELECT Video_Data_One.Video_Name, Video_Data_One.ViewCount,Channel_Five.Channel_Name  FROM Video_Data_One JOIN Channel_Five ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID ORDER BY Video_Data_One.ViewCount DESC LIMIT 10"
        column_names=['Video_Name','ViewCount','Channel_Name']
    elif option.startswith('4.'):
        query = "select Video_Name,CommentCount from Video_Data_One"
        column_names=['Video_Name','CommentCount']
    elif option.startswith('5.'):
        query = """SELECT Video_Name, Video_Data_One.LikeCount, Channel_Five.Channel_Name 
        FROM Video_Data_One JOIN Channel_Five 
        ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID 
        WHERE Video_Data_One.LikeCount = (SELECT MAX(LikeCount) FROM Video_Data_One)"""
        column_names=['Video_Name','LikeCount','Channel_Name']
    elif option.startswith('6.'):
        query = "select Video_Name,Video_Data_One.LikeCount,Video_Data_One.DisLikeCount from Video_Data_One"
        column_names=['Video_Name','LikeCount','DisLikeCount']
    elif option.startswith('7.'):
        query = "select Channel_Five.ViewCount,Channel_Name from Channel_Five"
        column_names=['ViewCount','Channel_Name']
    elif option.startswith('8.'):
        query = "select Channel_Five.Channel_Name,Channel_Five.PublishedAt from Channel_Five where YEAR(Channel_Five.PublishedAt)=2022"
        column_names=['Channel_Name','PublishedAt']
    elif option.startswith('9.'):
        query = '''SELECT Channel_Five.Channel_Name, AVG(Video_Data_One.Duration) AS Average_Duration_in_Seconds
          FROM Channel_Five JOIN Video_Data_One 
          ON Channel_Five.Channel_ID = Video_Data_One.Channel_ID GROUP BY Channel_Five.Channel_Name'''
        column_names=['Channel_Name','Average_Duration_InSeconds']
    elif option.startswith('10.'):
        query = "select Video_Data_One.Video_Name, Video_Data_One.CommentCount, Channel_Five.Channel_Name from Channel_Five JOIN Video_Data_One ON Video_Data_One.Channel_ID = Channel_Five.Channel_ID Where Video_Data_One.CommentCount=(select MAX(CommentCount) from Video_Data_One)"
        column_names=['Video_Name','Comment_Count','Channel_Name']
    else:
        st.write("Select the query from the DropDown Menu")
    
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
    else:
        st.write("No query selected")

    # Close the cursor and connection
    cursor.close()
    connection.close()  

if __name__ == "__main__":
    main()
