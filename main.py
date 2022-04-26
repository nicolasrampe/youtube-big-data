# API client library
import requests
import os
import json
import numpy as np
import pandas as pd
import tweepy
import googleapiclient.discovery
# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyBYwVqhlTzox2YdwHMk9ZKRQJkNkj2F2N0'
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
# Request body
request = youtube.search().list(
        part="id,snippet",
        regionCode= 'CO',
        type='video',
        q="Energías Renovables",
        videoDuration='short',
        videoDefinition='high',
        maxResults=50
)
# Request execution
response = request.execute()
print(response)