
#!/usr/bin/python
import praw
import re
import json
import atexit
import os



reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("uoft")


# Have we run this code before? If not, create an empty list
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

def exit_handler():
    # Write our updated list back to the file
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")

atexit.register(exit_handler)


comments = subreddit.stream.comments()

for comment in comments:
     # If we haven't replied to this post before
    if comment.id not in comments_replied_to:
        # Do a case insensitive search for the bot
        match = re.search("^\/u\/UofT-Bot \w*$", comment.body, re.IGNORECASE)
        if match:
            #Get the course code from the comment
            split_comment = re.split("\s", comment.body)
            with open('courses.json', 'r', errors='ignore') as json_file:
                json_course = json_file.readline()
                while json_course:
                    course = json.loads(json_course)
                    if re.search(split_comment[1], course['code'], re.IGNORECASE):
                        comment.reply(course['code'] + " - " + course["description"])
                        comments_replied_to.append(comment.id)
                        print("Replied!")
                        break
                    else:
                        json_course = json_file.readline()            


