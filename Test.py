import praw as praw
from praw.models import MoreComments
import os
import sys
import time

#gets shit from other classes when Test.py exists outside of src
sys.path.append(os.path.join(sys.path[0], 'src'))

SAVE_FILE_PATH = 'data/'
# This is equal to 15 minutes
SCHEDULE_TIME = 60.0 * 15.0
SELECTED_SUBREDDITS = ['funny', 'pics', 'gaming', 'aww', 'mildlyinteresting']
# These two are for testing purposes
SINGLE_SUBREDDIT = ['pubattlegrounds']
DOUBLE_SUBREDDIT = ['funny', 'pics']
#
NUM_OF_POSTS_TO_GRAB = 2
#example of importing a method from database

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')
jsonString = ''
subredditCount = 0
submissionsCount = 0
topCommentCount = 0
secondCommentCount = 0
thirdCommentCount = 0

starttime = time.time()

def formatCommonJSON(incoming):
    # This is for getting rid of duplicate code
    toReturn = ''

def grabInformation(incomingSubreddit):
    global jsonString
    global subredditCount
    subredditCount += 1
    jsonString += ('"subreddit'+ str(subredditCount) +'": {')
    jsonString += ('"name": "/r/' + incomingSubreddit +'",')
    jsonString += ('"all_posts": {')
    selectedReddit = reddit.subreddit(incomingSubreddit)
    for submission in selectedReddit.hot(limit=NUM_OF_POSTS_TO_GRAB):
        global submissionsCount
        submissionsCount += 1

        jsonString += ('"post'+ str(submissionsCount) +'": {')
        # This is the actual meat of the post
        jsonString += ('"title":"' + str(submission.title) + '",')
        jsonString += ('"author":"' + str(submission.author) + '",')
        jsonString += ('"time":"' + str(submission.created) + '",')
        jsonString += ('"score":"' + str(submission.score) + '",')
        jsonString += ('"id":"' + str(submission.id) + '",')
        jsonString += ('"url":"' + str(submission.url) + '",')
        submission.comments.replace_more(limit=0)
        jsonString += ('"all_comments": {')
        for top_level_comment in submission.comments:
            global topCommentCount
            topCommentCount += 1

            jsonString += ('"comment'+ str(topCommentCount) +'": {')

            jsonString += ('"author":"' + str(top_level_comment.author) +'",')
            jsonString += ('"time":"' + str(top_level_comment.created) + '",')
            jsonString += ('"score":"' + str(top_level_comment.score) + '",')
            jsonString += ('"id":"' + str(top_level_comment.id) + '",')
            formattedBody = top_level_comment.body.replace("'", "")
            formattedBody = formattedBody.replace('"', '')
            formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
            jsonString += ('"body":" ' + str(formattedBody) + ' ",')
            jsonString += ('"second_level_comments": {')
            if len(top_level_comment.replies) == 0:
                jsonString += ('}')
            for second_level_comment in top_level_comment.replies:
                global secondCommentCount
                secondCommentCount += 1

                jsonString += ('"comment' + str(secondCommentCount) + '": {')

                jsonString += ('"author":"' + str(second_level_comment.author) + '",')
                jsonString += ('"time":"' + str(second_level_comment.created) + '",')
                jsonString += ('"score":"' + str(second_level_comment.score) + '",')
                jsonString += ('"id":"' + str(second_level_comment.id) + '",')
                formattedBody = second_level_comment.body.replace("'", "")
                formattedBody = formattedBody.replace('"', '')
                formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
                jsonString += ('"body":" ' + str(formattedBody) + ' ",')
                jsonString += ('"third_level_comments": {')
                if len(second_level_comment.replies) == 0:
                    jsonString += ('}')
                for third_level_comment in second_level_comment.replies:
                    global thirdCommentCount
                    thirdCommentCount += 1

                    jsonString += ('"comment' + str(thirdCommentCount) + '": {')

                    jsonString += ('"author":"' + str(third_level_comment.author) + '",')
                    jsonString += ('"time":"' + str(third_level_comment.created) + '",')
                    jsonString += ('"score":"' + str(third_level_comment.score) + '",')
                    jsonString += ('"id":"' + str(third_level_comment.id) + '",')
                    formattedBody = third_level_comment.body.replace("'", "")
                    formattedBody = formattedBody.replace('"', '')
                    formattedBody = formattedBody.replace('\n', '').replace('\r', '').replace('\\', '\\\\')
                    jsonString += ('"body":" ' + str(formattedBody) + ' "')
                    if thirdCommentCount == len(second_level_comment.replies):
                        jsonString += ('}}')
                        thirdCommentCount = 0
                    else:
                        jsonString += ('},')
                #
                if secondCommentCount == len(top_level_comment.replies):
                    jsonString += ('}}')
                    secondCommentCount = 0
                else:
                    jsonString += ('},')
            if topCommentCount == len(submission.comments):
                jsonString += ('}')
                topCommentCount = 0
            else:
                jsonString += ('},')
        if(submissionsCount == NUM_OF_POSTS_TO_GRAB):
            jsonString += ('}}')
            submissionsCount = 0
        else:
            jsonString += ('}},')
    # The array used in this needs to be the same as the one in the while loop
    if subredditCount == len(SELECTED_SUBREDDITS):
        jsonString += ('}}')
    else:
        jsonString += ('}},')


while True:
    jsonString += ("{")
    jsonString += ('"Reddit_Object":[')
    jsonString += ("{")
    for sub in SELECTED_SUBREDDITS:
        grabInformation(sub)
    jsonString += ('}]}')
    file = open(SAVE_FILE_PATH + str(round(time.time())) + ".txt", "w")
    file.write(str(jsonString))
    file.close()
    print(str(round(time.time())) + " finished")
    jsonString = ''
    time.sleep(SCHEDULE_TIME -((time.time() - starttime) % SCHEDULE_TIME))
