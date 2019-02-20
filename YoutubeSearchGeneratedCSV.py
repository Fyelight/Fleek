#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
import urllib.parse
import csv

import config as cfg # from config.py


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
YOUTUBE_V_URL_HEAD = 'https://www.youtube.com/watch?v='
DEVELOPER_KEY = cfg.cfg["DEVELOPER_KEY"]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#csv file input for search criteria
fileDir = "C:\\Users\\KaiDF\\Desktop\\Fleek\\train_label.csv"
outDir = "C:\\Users\KaiDF\\Desktop\\"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []
    videoUrl = []
    #
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s | %s (%s) [%s]' % (search_result['snippet']['channelTitle'],
                                            search_result['snippet']['title'],
                                            search_result['snippet']['description'],
                                            search_result['id']['videoId']))
            videoUrl.append(YOUTUBE_V_URL_HEAD + search_result['id']['videoId'])
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                         search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                          search_result['id']['playlistId']))

    print('Videos:\n', '\n'.join(videos), '\n')
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')
    print(videoUrl)

    # search_string = "test !@#$^*( test"
    # print(urllib.parse.quote_plus(search_string))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s', e.resp.status, e.content)


def run(rdr):
    i = 0
    for row in rdr:
        if i == 0:
            print(row)  # header
            continue
        i += 1
    print(i)
    with open(outDir + "q1.csv", "w", newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        # writer.writeheader(rdr.fieldnames)
        for row in rdr:
            writer.writerow(row)


# with open(fileDir, newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     run(reader)
