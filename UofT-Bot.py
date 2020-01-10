
#!/usr/bin/python
import praw
#import pdb
import re
import os
import json
#import requests


reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("uoft")

with open('courses.json', 'r') as json_file:
    course = json.loads(json_file.readline())
    print(course['code'])



# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))




for submission in subreddit.hot(limit=50):
    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        if re.search("csc", submission.title, re.IGNORECASE):
            # Reply to the post
            #submission.reply("Nigerian scammer bot says: It's all about the Bass (and Python)")
            print("Bot replying to : ", submission.title)

            # Store the current id into our list
            posts_replied_to.append(submission.id)




# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")