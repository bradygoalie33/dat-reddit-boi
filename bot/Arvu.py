import praw as praw
import datetime
from random import randint
import time
from praw.models import MoreComments

# After a viewing session I want to log the posts and comments Arvu viewed so that if he goes down he can keep track of
# what he's already looked at.
#       Along with that we'll need an init so that he can read that file and throw those posts into his viewed_posts
#       Also along with that he needs comment viewing validation
# After a viewing session I want Arvu to log information about what he's done.
#   ex: length of session, start/end of session, num of posts/comments viewed, upvotes, downvotes, saves

PERCENTAGE_TO_UPVOTE_POST = 10
PERCENTAGE_TO_DOWNVOTE_POST = 2
PERCENTAGE_TO_UPVOTE_COMMENT = 10
PERCENTAGE_TO_DOWNVOTE_COMMENT = 8
PERCENTAGE_TO_VIEW_POST = 80

# This one is 1/3 of int
PERCENTAGE_TO_SAVE_POST = 1

# This is 9 AM
ACTIVE_HOUR_START = 32400
# This is 5 PM (Using this for normal bot behavior
# ACTIVE_HOUR_END = 61200
# This is 10 PM (Using this for working while I'm at home)
ACTIVE_HOUR_END = 79200

DEBUG = True

reddit = praw.Reddit(client_id='El479iqdfj-v0g',
                     client_secret='_2lWTM5i_USFV4Aynn_k_p-ySOo',
                     password='TeamHandsome',
                     user_agent='Test script by /u/EverestAtlas',
                     username='EverestAtlas')

viewed_posts = []


def should_save_post():
    percent_chance = randint(0, 300)
    if percent_chance == PERCENTAGE_TO_SAVE_POST:
        return True
    return False


def should_upvote_post():
    percent_chance = randint(0, 100)
    if percent_chance <= PERCENTAGE_TO_UPVOTE_POST:
        return True
    return False


def should_downvote_post():
    percent_chance = randint(0, 100)
    if percent_chance <= PERCENTAGE_TO_DOWNVOTE_POST:
        return True
    return False


def should_upvote_comment():
    percent_chance = randint(0, 100)
    if percent_chance <= PERCENTAGE_TO_UPVOTE_COMMENT:
        return True
    return False


def should_downvote_comment():
    percent_chance = randint(0, 100)
    if percent_chance <= PERCENTAGE_TO_DOWNVOTE_COMMENT:
        return True
    return False



def should_view_post():
    percent_chance = randint(0, 100)
    if percent_chance <= PERCENTAGE_TO_VIEW_POST:
        return True
    return False


def how_many_comments_to_view(total_top_comments):
    num_of_comments = randint(0, round(total_top_comments/5))
    print('numToView: ' + str(num_of_comments))
    return num_of_comments


def sleep_between_comment_views():
    sleep_time = randint(0, 5)
    print('comment sleep: ' + str(sleep_time))
    if DEBUG:
        return 0
    return sleep_time


def sleep_between_post_views():
    sleep_time = randint(0, 20)
    print("post sleep: " + str(sleep_time))
    if DEBUG:
        return 0
    return sleep_time


def sleep_between_viewing_sessions():
    sleep_time = randint(10, 120)
    sleep_time = sleep_time * 60
    print("view sleep: " + str(sleep_time))
    if DEBUG:
        return 0
    return sleep_time


def view_comment(comment):
    print(comment.body)
    if should_upvote_comment():
        print("SHOULD UPVOTE COMMENT")
        return True
    elif should_downvote_comment():
        print("SHOULD DOWNVOTE COMMENT")
    return False


def view_post(post):
    global viewed_posts
    print(post.title)
    if post.id not in viewed_posts:
        if should_view_post:
            viewed_posts.append(post.id)
            if should_upvote_post():
                print("SHOULD UPVOTE POST")
            elif should_downvote_post():
                print("SHOULD DOWNVOTE POST")
            if should_save_post():
                print("SHOULD SAVE POST!!")
            top_level_comment_array = []
            second_level_comment_array = []
            for top_level_comment in post.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                top_level_comment_array.append(top_level_comment)

            for comment_num in range(how_many_comments_to_view(len(top_level_comment_array))):
                did_upvote = view_comment(top_level_comment_array[comment_num])
                if did_upvote:
                    if(len(top_level_comment_array[comment_num].replies) > 0):
                        view_comment(top_level_comment_array[comment_num].replies[0])
                time.sleep(sleep_between_comment_views())
        else:
            print("VIEW SKIP")
        time.sleep(sleep_between_post_views())
    else:
        print("ALREADY VIEWED")


def get_frontpage_of_all():
    submission_array = []
    selected_subreddit = reddit.subreddit('all')
    for submission in selected_subreddit.hot(limit=150):
        submission_array.append(submission)
    return submission_array


while True:
    # This grabs the time now and puts it into seconds since midnight
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date(), datetime.time())
    current_time_in_seconds = (now - midnight).seconds

    unformatted_view_time = randint(0, 15)
    view_time = unformatted_view_time * 60
    if DEBUG:
        end_of_viewing_session = current_time_in_seconds + 15
    else:
        end_of_viewing_session = current_time_in_seconds + view_time

    if ACTIVE_HOUR_START < current_time_in_seconds < ACTIVE_HOUR_END:
        submissions = get_frontpage_of_all()
        for post in submissions:
            now = datetime.datetime.now()
            current_time = (now - midnight).seconds
            if current_time < end_of_viewing_session:
                view_post(post)
            else:
                print('time is up')
                break
        time.sleep(sleep_between_viewing_sessions())