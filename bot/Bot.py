import praw as praw
import datetime
from random import randint
import time

# We need to keep track of what posts we've already viewed so that we don't view them twice.

# This is 9 AM
from praw.models import MoreComments

ACTIVE_HOUR_START = 32400
# This is 5 PM
# ACTIVE_HOUR_END = 61200
# This is 10 PM (Using this for working while I'm at home)
ACTIVE_HOUR_END = 79200

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='Test script by /u/EverestAtlas',
                     username='EverestAtlas')

viewed_posts = []


def should_save_post():
    percent_chance = randint(0, 300)
    if percent_chance == 1:
        return True
    return False


def should_upvote_post():
    percent_chance = randint(0, 100)
    if percent_chance <= 10:
        return True
    return False


def should_upvote_comment():
    percent_chance = randint(0, 100)
    if percent_chance <= 30:
        return True
    return False


def should_view_post():
    percent_chance = randint(0, 100)
    if percent_chance >= 20:
        return True
    return False


def how_many_comments_to_view(total_top_comments):
    num_of_comments = randint(0, round(total_top_comments/4))
    print('numToView: ' + str(num_of_comments))
    return num_of_comments


def sleep_between_comment_views():
    sleep_time = randint(0, 5)
    print('comment sleep: ' + str(sleep_time))
    return sleep_time


def sleep_between_post_views():
    sleep_time = randint(0, 20)
    print("post sleep: " + str(sleep_time))
    return sleep_time


def sleep_between_viewing_sessions():
    sleep_time = randint(10, 120)
    sleep_time = sleep_time * 60
    print("view sleep: " + str(sleep_time))
    return sleep_time


def view_comment(comment):
    print(comment.body)
    if should_upvote_comment():
        print("SHOULD UPVOTE COMMENT")


def view_post(post):
    global viewed_posts
    print(post.title)
    if post.id not in viewed_posts:
        if should_view_post:
            viewed_posts.append(post.id)
            if should_upvote_post():
                print("SHOULD UPVOTE POST")
            if should_save_post():
                print("SHOULD SAVE POST!!")
            top_level_comment_array = []
            second_level_comment_array = []
            for top_level_comment in post.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
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
    for submission in selected_subreddit.hot(limit=100):
        submission_array.append(submission)
    return submission_array


while True:
    # This grabs the time now and puts it into seconds since midnight
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date(), datetime.time())
    current_time_in_seconds = (now - midnight).seconds

    unformatted_view_time = randint(0, 15)
    view_time = unformatted_view_time * 60
    end_of_viewing_session = current_time_in_seconds + view_time

    if ACTIVE_HOUR_START < current_time_in_seconds < ACTIVE_HOUR_END:
        submissions = get_frontpage_of_all()
        for post in submissions:
            now = datetime.datetime.now()
            midnight = datetime.datetime.combine(now.date(), datetime.time())
            current_time = (now - midnight).seconds
            if current_time < end_of_viewing_session:
                view_post(post)
            else:
                print('time is up')
                time.sleep(sleep_between_viewing_sessions())
                break
        time.sleep(sleep_between_viewing_sessions())