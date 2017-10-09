import praw as praw
import datetime

# This is 9 AM
ACTIVE_HOUR_START = 32400
# This is 5 PM
ACTIVE_HOUR_END = 61200

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='testscript by /u/EverestAtlas',
                     username='EverestAtlas')

# for submission in reddit.front.hot():
#     print(submission.title)

while True:
    # This grabs the time now and puts it into seconds since midnight
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date(), datetime.time())
    current_time_in_seconds = (now - midnight).seconds

    print(current_time_in_seconds)
    if current_time_in_seconds > ACTIVE_HOUR_START and current_time_in_seconds < ACTIVE_HOUR_END :
        print('yes')