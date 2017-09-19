from pprint import pprint
import numpy
import praw as praw
from praw.models import MoreComments
import requests
import json
import os
import sys
import sched, time

#gets shit from other classes when Test.py exists outside of src
sys.path.append(os.path.join(sys.path[0], 'src'))

# This is equal to 15 minutes
SCHEDULE_TIME = 60.0 * 15.0
SELECTED_SUBREDDITS = ['funny', 'pics', 'gaming', 'aww', 'mildlyinteresting']
SINGLE_SUBREDDIT = ['pubattlegrounds']
#example of importing a method from database
# from src import database
from src import Comment

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

# print(reddit.user.me())



starttime = time.time()
def grabInformation(incomingSubreddit):
    # file = open(str(round(time.time())) + ".txt", "w")

    subredditSubmissions = []
    # This section grabs info from the subreddit /r/funny and displays info about it
    selectedReddit = reddit.subreddit(incomingSubreddit)
    for submission in selectedReddit.hot(limit=2):
        # print('/r/' + incomingSubreddit)
        # print(submission.title)
        # print(submission.author)
        # print(submission.score)
        # print(submission.id)
        subredditSubmissions.append(submission)
        # print(submission.url)
        # print("\n")

    # This section goes through all the posts I've gotten from above and grabs the top level comments from each one
    # print("Comments Here: ")
    #
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        newComment = Comment.TopLevelComment(top_level_comment)
        # print(newComment.printout())
        # print(top_level_comment.author)
        for second_level_comment in top_level_comment.replies:
            newComment.commentChildren.append(second_level_comment)
            # print("\nSECOND: " + second_level_comment.body)
        #     for third_level_comment in second_level_comment.replies:
        #         print("THIRD: " + third_level_comment.body)
    print("\nTREE: " + str(len(newComment.commentChildren)))
    # file.close()


while True:
    for sub in SINGLE_SUBREDDIT:
        grabInformation(sub)
    time.sleep(SCHEDULE_TIME -((time.time() - starttime) % SCHEDULE_TIME))
