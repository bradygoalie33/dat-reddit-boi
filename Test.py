from pprint import pprint

import praw as praw
from praw.models import MoreComments

import requests
import json
import os
import sys
import sched, time

#gets shit from other classes when Test.py exists outside of src
sys.path.append(os.path.join(sys.path[0], 'src'))

#example of importing a method from database
from database import execute_query

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

# print(reddit.user.me())



starttime = time.time()

def grabInformation():
    subredditIds = []
    # This section grabs info from the subreddit /r/funny and displays info about it
    funny = reddit.subreddit('funny')
    for submission in funny.hot(limit=2):
        print(submission.title)
        print(submission.author)
        print(submission.score)
        print(submission.id)
        subredditIds.append(submission.id)
        print(submission.url)
        print("\n")

    # This section goes through all the posts I've gotten from above and grabs the top level comments from each one
    print("Comments Here: ")

    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        print("TOP: " + top_level_comment.body)
        for second_level_comment in top_level_comment.replies:
            print("\nSECOND: " + second_level_comment.body)
            for third_level_comment in second_level_comment.replies:
                print("THIRD: " + third_level_comment.body)
    print("\n")


while True:
    grabInformation()
    time.sleep(60.0 -((time.time() - starttime) % 60.0))
