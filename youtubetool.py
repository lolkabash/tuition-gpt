
import os
from urllib.request import urlopen
import json
from dotenv import load_dotenv
import requests


#provide API key here
load_dotenv()
YOUTUBE_API_KEY = os.getenv("youtube_api_key")


channel_id_list = ['UCX6b17PVsYBQ0ip5gyeme-Q', 'UCEWpbFLzoYGPfuWUMFPSaoA']
channel_name_list = ['CrashCourse', 'The Organic Chemistry Tutor']
KEYWORDS = ['Momentum Conservation Principle', 'system undergoing recoil', 'elastic collision']  


def channelid(ans):
    #to eliminate spaces between search queries with %20
    str1='%20'.join([str(ele) for ele in ans])
    #Use yt API to give search results for username
    site1=urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+str1 +'&type=channel&key='+YOUTUBE_API_KEY)
    #loads data to a json file format
    a1 = json.load(site1)
    #to get channelid and channelname using username
    ucid=str(a1.get("items")[0].get("id").get('channelId'))
    channelname=a1.get("items")[0].get("snippet").get('title')
    #returns channelid & channelname
    return(ucid,channelname)


def create_channel_id_list():
    """creates a list of youtube channel IDs given an input of channel names"""
    keep_adding = True
    channel_id_list = []
    while keep_adding:
        ans1=str(input('Input Username : ' )).split()
        channel_id,name=channelid(ans1)
        channel_id_list.append(channel_id)
        channel_name_list.append(name)
        resume = input("keep adding? y/n")
        if resume == "n":
            keep_adding = False
    return channel_id_list


# def returnurl(ucid):
#     #creates and returns url for statistics usin channelid
#     u='https://www.googleapis.com/youtube/v3/channels?id='+ucid+'&key='+API_KEY+'&part=statistics'
#     return(u)

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
            'maxResults': 1,  # You can adjust this number
            'key': api_key
        }
        response = requests.get(base_url, params=params).json()
        for item in response.get('items', []):
            video_title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            videos.append((video_title, video_url))

    return videos


def retrieve_videos():
    """main fucntion of this module to be called. it will return a nested dictionary, ie {keyword:{video_title:url,..}, keyword...}"""
    video_library = {}
    for keyword in KEYWORDS:
        found_videos = search_videos(YOUTUBE_API_KEY,channel_id_list , keyword)
        video_library[keyword] = {title:url for title, url in found_videos}
    return video_library



# {'Momentum Conservation Principle': {'The Law of Conservation: Crash Course Engineering #7': 'https://www.youtube.com/watch?v=VxCORJ8dN3Y',
#                                       'Conservation of Momentum Physics Problems - Basic Introduction': 'https://www.youtube.com/watch?v=Fp7D5D8Bqjc'},
#  'system undergoing recoil': {'Elastic Collisions In One Dimension Physics Problems - Conservation of Momentum &amp; Kinetic Energy': 'https://www.youtube.com/watch?v=CFbo_nBdBco'},
#  'elastic collision': {'Collisions: Crash Course Physics #10': 'https://www.youtube.com/watch?v=Y-QOfc2XqOk',
#                         'Elastic Collisions In One Dimension Physics Problems - Conservation of Momentum &amp; Kinetic Energy': 'https://www.youtube.com/watch?v=CFbo_nBdBco'}
#  }

