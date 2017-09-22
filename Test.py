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
DOUBLE_SUBREDDIT = ['funny', 'pics']
NUM_OF_POSTS_TO_GRAB = 2
#example of importing a method from database
# from src import database
from src import Comment

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

subredditCount = 0
submissionsCount = 0
topCommentCount = 0
secondCommentCount = 0
thirdCommentCount = 0

starttime = time.time()
def grabInformation(incomingSubreddit):
    # file = open(str(round(time.time())) + ".txt", "w")

    global subredditCount
    subredditCount += 1
    print('"subreddit'+ str(subredditCount) +'": {')
    print('"name": "/r/' + incomingSubreddit +'",')
    print('"all_posts": {')
    selectedReddit = reddit.subreddit(incomingSubreddit)
    for submission in selectedReddit.hot(limit=NUM_OF_POSTS_TO_GRAB):
        global submissionsCount
        submissionsCount += 1

        print('"post'+ str(submissionsCount) +'": {')

        print('"title":"' + str(submission.title) + '",')
        print('"author":"' + str(submission.author) + '",')
        print('"score":"' + str(submission.score) + '",')
        print('"id":"' + str(submission.id) + '",')
        print('"url":"' + str(submission.url) + '",')
        submission.comments.replace_more(limit=0)
        print('"all_comments": {')
        for top_level_comment in submission.comments:
            global topCommentCount
            topCommentCount += 1

            print('"comment'+ str(topCommentCount) +'": {')

            print('"author":"' + str(top_level_comment.author) +'",')
            print('"score":"' + str(top_level_comment.score) + '",')
            print('"id":"' + str(top_level_comment.id) + '",')
            formattedBody = top_level_comment.body.replace("'", "")
            formattedBody = formattedBody.replace('"', '')
            formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
            print('"body":" ' + str(formattedBody) + ' ",')
            print('"second_level_comments": {')
            if len(top_level_comment.replies) == 0:
                print('}')
            for second_level_comment in top_level_comment.replies:
                global secondCommentCount
                secondCommentCount += 1

                print('"comment' + str(secondCommentCount) + '": {')

                print('"author":"' + str(second_level_comment.author) + '",')
                print('"score":"' + str(second_level_comment.score) + '",')
                print('"id":"' + str(second_level_comment.id) + '",')
                formattedBody = second_level_comment.body.replace("'", "")
                formattedBody = formattedBody.replace('"', '')
                formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
                print('"body":" ' + str(formattedBody) + ' ",')
                print('"third_level_comments": {')
                if len(second_level_comment.replies) == 0:
                    print('}')
                #
                for third_level_comment in second_level_comment.replies:
                    global thirdCommentCount
                    thirdCommentCount += 1

                    print('"comment' + str(thirdCommentCount) + '": {')

                    print('"author":"' + str(third_level_comment.author) + '",')
                    print('"score":"' + str(third_level_comment.score) + '",')
                    print('"id":"' + str(third_level_comment.id) + '",')
                    formattedBody = third_level_comment.body.replace("'", "")
                    formattedBody = formattedBody.replace('"', '')
                    formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
                    print('"body":" ' + str(formattedBody) + ' "')
                    if thirdCommentCount == len(second_level_comment.replies):
                        print('}}')
                        thirdCommentCount = 0
                    else:
                        print('},')
                #
                if secondCommentCount == len(top_level_comment.replies):
                    print('}}')
                    secondCommentCount = 0
                else:
                    print('},')
            if topCommentCount == len(submission.comments):
                print('}')
                topCommentCount = 0
            else:
                print('},')
        if(submissionsCount == NUM_OF_POSTS_TO_GRAB):
            print('}}')
            submissionsCount = 0
        else:
            print('}},')
    # The array used in this needs to be the same as the one in the while loop
    if subredditCount == len(SELECTED_SUBREDDITS):
        print('}}')
    else:
        print('}},')


while True:
    print("{")
    print('"Reddit_Object":[')
    print("{")
    for sub in SELECTED_SUBREDDITS:
        grabInformation(sub)
    print('}]}')
    time.sleep(SCHEDULE_TIME -((time.time() - starttime) % SCHEDULE_TIME))
