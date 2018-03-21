#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python geolocation_search.py --q=surfing --location-"37.42307,-122.08427" --location-radius=50km --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDd764fbXguz6wvDt0glc7_CSxuQF2ZbBc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
f = open("test.csv", "w") 
f.write("trailer_id,title,uploadDate,totalViews,noOfLikes,noOfDislikes,totalComment\n")

def youtube_search(options):
  global videos
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  print "***"

  search_response = youtube.search().list(
      q=options.q,
      type='video',
      part='id,snippet',
      order='relevance',
      maxResults=options.max_results
    ).execute()

  search_videos = []

  for search_result in search_response.get('items', []):
    # if search_result['id']['kind'] == 'youtube#video':
    search_videos.append(search_result['id']['videoId'])
  video_ids = ','.join(search_videos)

  # Call the videos.list method to retrieve location details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet,statistics'
  ).execute()

  
  trailer_count=0
  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get('items', []):
    trailer_count=trailer_count+1
    string =str( "%s, %s, %s, %s, %s, %s" %(video_result['snippet']['title'].encode('ascii', 'ignore').replace(","," | "),
                              video_result['snippet']['publishedAt'].encode('ascii', 'ignore'),
                              video_result['statistics']['viewCount'].encode('ascii', 'ignore'),
                              video_result['statistics']['likeCount'].encode('ascii', 'ignore'),
                              video_result['statistics']['dislikeCount'].encode('ascii', 'ignore'),
                              video_result['statistics']['commentCount'].encode('ascii', 'ignore')))
    print string
    f.write(str(trailer_count)+","+string+"\n")

  search_response = youtube.search().list(
      q=options.q,
      type='video',
      part='id,snippet',
      maxResults=options.max_results,
    ).execute()

  nextPageToken = search_response.get("nextPageToken","")  

  for i in range(int(options.num_pages)-1):
    # Call the search.list method to retrieve results matching the specified
    # query term.    
    print "***"
    search_response = youtube.search().list(
      q=options.q,
      type='video',
      part='id,snippet',
      order='relevance',
      pageToken=nextPageToken,
      maxResults=options.max_results
    ).execute()

    search_videos = []

    # Merge video ids
    for search_result in search_response.get('items', []):
      search_videos.append(search_result['id']['videoId'])
    video_ids = ','.join(search_videos)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
      id=video_ids,
      part='snippet,statistics'
    ).execute()

    
    # Add each result to the list, and then display the list of matching videos.
    for video_result in video_response.get('items', []):
      trailer_count=trailer_count+1
      string =str( "%s, %s, %s, %s, %s, %s" %(video_result['snippet']['title'].encode('ascii', 'ignore').replace(","," | "),
                                video_result['snippet']['publishedAt'].encode('ascii', 'ignore'),
                                video_result['statistics']['viewCount'].encode('ascii', 'ignore'),
                                video_result['statistics']['likeCount'].encode('ascii', 'ignore'),
                                video_result['statistics']['dislikeCount'].encode('ascii', 'ignore'),
                                video_result['statistics']['commentCount'].encode('ascii', 'ignore')))
      print string
      f.write(str(trailer_count)+","+string+"\n")

    search_response = youtube.search().list(
      q=options.q,
      type='video',
      part='id,snippet',
      maxResults=options.max_results,
      pageToken=nextPageToken
    ).execute()

    nextPageToken = search_response.get("nextPageToken","")

    

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=25)
  parser.add_argument('--num-pages', help='Number Of Pages', default=1)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
