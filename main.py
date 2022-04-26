# API client library
import json

import googleapiclient.discovery as youtube
import pathlib

# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyBYwVqhlTzox2YdwHMk9ZKRQJkNkj2F2N0'
# API client
youtube = youtube.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_comments(video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
  ).execute()
def createjson_Videos(regionCode, keyWord):
    request = youtube.search().list(
        part="id,snippet",
        regionCode=regionCode,
        type='video',
        q=keyWord,
        videoDuration='short',
        videoDefinition='high',
        maxResults=50
    )
    # Request execution
    search_response = request.execute()
    for search_result in search_response.get("items", []):
        get_comments(search_result["id"]["videoId"])


    print(response)
    with open("./json/" + regionCode + "Videos.json", "w") as outfile:
        json.dump(response, outfile)


# Request body
createjson_Videos()
