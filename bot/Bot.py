import praw as praw
import datetime
from random import randint
import time

# We need to keep track of what posts we've already viewed so that we don't view them twice.

# This is 9 AM
ACTIVE_HOUR_START = 32400
# This is 5 PM
ACTIVE_HOUR_END = 61200

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='Test script by /u/EverestAtlas',
                     username='EverestAtlas')


def should_upvote_post():
    percent_chance = randint(0, 100)
    if percent_chance >= 10:
        return True
    return False


def should_upvote_comment():
    percent_chance = randint(0, 100)
    if percent_chance >= 30:
        return True
    return False


def how_many_comments_to_view(total_top_comments):
    num_of_comments = randint(0, round(total_top_comments/4))
    print('numToView: ' + str(num_of_comments))
    return num_of_comments


def sleep_between_comment_views():
    sleep_time = randint(0, 15)
    print('comment sleep: ' + str(sleep_time))
    return sleep_time


def sleep_between_post_views():
    sleep_time = randint(0, 60)
    print("post sleep: " + str(sleep_time))
    return sleep_time


def view_comment(comment):
    print(comment.body)


def view_post(post):
    print(post.title)
    top_level_comment_array = []
    second_level_comment_array = []
    for top_level_comment in post.comments:
        top_level_comment_array.append(top_level_comment)
        for second_level_comment in top_level_comment.replies:
            second_level_comment_array.append(second_level_comment)

    for comment_num in range(how_many_comments_to_view(len(top_level_comment_array))):
        view_comment(top_level_comment_array[comment_num])
        time.sleep(sleep_between_comment_views())

    time.sleep(sleep_between_post_views())


def get_frontpage_of_all():
    submission_array = []
    selected_subreddit = reddit.subreddit('all')
    for submission in selected_subreddit.hot(limit=25):
        submission_array.append(submission)
    return submission_array


while True:
    # This grabs the time now and puts it into seconds since midnight
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date(), datetime.time())
    current_time_in_seconds = (now - midnight).seconds

    if ACTIVE_HOUR_START < current_time_in_seconds < ACTIVE_HOUR_END:
        submissions = get_frontpage_of_all()
        for post in submissions:
            view_post(post)
