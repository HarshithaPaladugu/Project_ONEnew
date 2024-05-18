# Project_ONEnew
FinalTABLES_New.py file contains code to create amd insert the data in to the channel table. And fetch the data related to video and comments.
video_data_one table:

Database Connection: The code establishes a connection to a MySQL database named 'YoutubeDataHarvesting' running on the localhost using the credentials provided.
Function Definitions:
get_all_video_ids(c_id): This function retrieves all video IDs associated with a given channel ID using the YouTube Data API. It iterates through the playlist items of the channel's 'uploads' playlist to collect the video IDs.
get_video_details(v_id): This function retrieves details of a specific video given its video ID using the YouTube Data API. It gathers information such as video name, channel ID, duration, view count, like count, dislike count, and comment count.
Table Creation: The code checks if a table named 'Video_Data_One' exists in the database. If not, it creates the table with columns for storing video details.
Data Retrieval and Update:
For each channel ID in the channel_ids list, the code retrieves all video IDs associated with that channel using get_all_video_ids(c_id).
For each video ID obtained, it retrieves video details using get_video_details(v_id).
It then checks if each video already exists in the database based on its name.
If the video exists, it updates its data in the database. If not, it inserts a new entry.
Finally, it commits the changes to the database.
Data Retrieval for Verification: After updating the database, the code fetches all data from the 'Video_Data_One' table and displays it as a Pandas DataFrame for verification.
Channel_Five table:

Global YouTube Object: A global youtube object is defined to hold the YouTube Data API instance.
Database Connection: The code establishes a connection to a MySQL database named 'YoutubeDataHarvesting' running on the localhost using the provided credentials.
API Connection Function: The api_connect() function initializes the global youtube object by building a connection to the YouTube Data API using the developer key.
Function to Get Channel Details: The get_channel_details(channel_id) function takes a channel ID as input and retrieves details about the channel using the YouTube Data API. It extracts information such as the channel name, description, playlist ID, view count, video count, subscriber count, and publishing date.
Table Creation: The code checks if a table named 'Channel_Five' exists in the database. If not, it creates the table with columns to store channel details.
Define Channel IDs: A list of channel IDs is defined to specify the channels for which details need to be fetched.
Iterate Through Channel IDs: The code iterates through each channel ID in the channel_ids list.
Fetch Channel Details: For each channel ID, it establishes a connection to the YouTube Data API, fetches the channel details using get_channel_details(channel_id), and stores them in the channel_details variable.
Insert Channel Details into Database: It then inserts the channel details into the 'Channel_Five' table in the database using an INSERT IGNORE query to avoid inserting duplicate entries.
Fetch Data from Database: After inserting the data, it fetches all data from the 'Channel_Five' table in the database and converts it into a Pandas DataFrame for easy visualization and verification.
Display Data: Finally, it prints the DataFrame containing the fetched channel details.
Similarly the data related to videos and comments are fetched from the database. 

FINALApp.py:

This Streamlit app interacts with a MySQL database and the YouTube Data API to perform various queries and display the results based on user input. Here's the flow of execution:

Database Connection Function: The connect_to_database() function establishes a connection to the MySQL database.
Streamlit App Setup: The main() function initializes the Streamlit app, sets the app title, and provides a select box for the user to choose from a list of channel IDs.
Fetching Channel Information: When the user clicks the "Submit" button, the app executes a query to fetch channel information based on the selected channel ID. If data is found, it creates a DataFrame and displays the channel information.
Selecting Query Option: The app provides a dropdown menu for the user to select different query options. Each option corresponds to a specific query to be executed.
Executing Query: When the user clicks the "Execute the Query" button, the selected query is executed, and the result is displayed in a DataFrame.
Query Execution: Based on the selected query option, the app executes the corresponding SQL query. If the query involves fetching data from the database, it fetches the result and displays it. If the query requires interaction with the YouTube Data API, it executes the appropriate API call and displays the result.
Displaying Result: The result of the executed query is displayed in a DataFrame format within the Streamlit app.
Closing Connection: After the user finishes interacting with the app, the database cursor and connection are closed to release resources.
The Output of the following queries are displayed in the streamlit app upon selection of the query to be executed from the dropdown menu.
1. What are the names of all the videos and their corresponding channels?
2. Which channels have the most number of videos, and how many videos do
they have?
3. What are the top 10 most viewed videos and their respective channels?
4. How many comments were made on each video, and what are their
corresponding video names?
5. Which videos have the highest number of likes, and what are their
corresponding channel names?
6. What is the total number of likes and dislikes for each video, and what are
their corresponding video names?
7. What is the total number of views for each channel, and what are their
corresponding channel names?
8. What are the names of all the channels that have published videos in the year
2022?
9. What is the average duration of all videos in each channel, and what are their
corresponding channel names?
10.Which videos have the highest number of comments, and what are their
corresponding channel names?
