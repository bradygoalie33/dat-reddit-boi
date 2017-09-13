from pprint import pprint

import praw as praw
from praw.models import MoreComments

import requests
import json

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

print(reddit.user.me())


subredditIds = []

# This section grabs info from the subreddit /r/funny and displays info about it
funny = reddit.subreddit('funny')
for submission in funny.hot(limit=25):
    print(submission.title)
    print(submission.score)
    print(submission.id)
    subredditIds.append(submission.id)
    print(submission.url)
    print(submission.author)
    print("\n")

# This section goes through all the posts I've gotten from above and grabs the top level comments from each one
print("Comments Here: ")
for id in subredditIds:
    submission = reddit.submission(id=id)
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        print(top_level_comment.body)
    print("END OF CURRENT COMMENT TREE\n")