
import os
from urllib.request import urlopen
import json
from dotenv import load_dotenv


#provide API key here
load_dotenv()
key=os.getenv("youtube_api_key")

# Replace with your actual API key, channel IDs, and keywords

channel_id_list = ['UCX6b17PVsYBQ0ip5gyeme-Q', 'UC_SvYP0k05UKiJ_2ndB02IA', 'UCEWpbFLzoYGPfuWUMFPSaoA']
channel_name_list = ['CrashCourse', 'blackpenredpen', 'The Organic Chemistry Tutor']
# keep_adding = True
# while keep_adding:
#     ans1=str(input('Input Username : ' )).split()
#     channel_id,name=channelid(ans1)
#     channel_id_list.append(channel_id)
#     channel_name_list.append(name)
#     resume = input("keep adding? y/n")
#     if resume == "n":
#         keep_adding = False
resource_dictionary = dict(zip(channel_name_list,channel_id_list))
print(resource_dictionary)

API_KEY = os.getenv("youtube_api_key")
channel_id_list = ['UCX6b17PVsYBQ0ip5gyeme-Q', 'UC_SvYP0k05UKiJ_2ndB02IA', 'UCEWpbFLzoYGPfuWUMFPSaoA']
KEYWORDS = 'momentum'  

def channelid(ans):
    #to eliminate spaces between search queries with %20
    str1='%20'.join([str(ele) for ele in ans])
    #Use yt API to give search results for username
    site1=urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+str1 +'&type=channel&key='+API_KEY)
    #loads data to a json file format
    a1 = json.load(site1)
    #to get channelid and channelname using username
    ucid=str(a1.get("items")[0].get("id").get('channelId'))
    channelname=a1.get("items")[0].get("snippet").get('title')
    #returns channelid & channelname
    return(ucid,channelname)
    
    
def returnurl(ucid):
    #creates and returns url for statistics usin channelid
    u='https://www.googleapis.com/youtube/v3/channels?id='+ucid+'&key='+API_KEY+'&part=statistics'
    return(u)



import requests

def search_videos(api_key, channel_ids, keywords):
    """Search for videos in specific channels with keywords."""
    videos = []
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    
    for channel_id in channel_ids:
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'q': keywords,
            'maxResults': 5,  # You can adjust this number
            'key': api_key
        }
        response = requests.get(base_url, params=params).json()
        for item in response.get('items', []):
            video_title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            videos.append((video_title, video_url))

    return videos



found_videos = search_videos(API_KEY,channel_id_list , KEYWORDS)
for title, url in found_videos:
    print(f'Video Title: {title}\nVideo URL: {url}\n')
