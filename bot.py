import re
import praw
import time


class MonitorBot:
    def __init__(self, subreddits, words, user_to_alert=''):
        # Transform subreddits array into a single string seperated by +'s
        subreddits = '+'.join(subreddits)
        print subreddits

        # assign member variables
        self.subreddits = subreddits
        self.words = words
        self.user_to_alert = user_to_alert

        # a variable to check if this is the first time we're grabbing threads
        self.first_time = True

        # an array to keep track of threads we've already seen
        self.seen_threads = []

        # Keep track of comments we've looked at
        self.seen_comments = []

        # create reddit client
        self.client = self.setup_reddit_client()

    def setup_reddit_client(self):
        # Provide a descriptive user-agent string. Explain what your bot does, reference
        # yourself as the author, and offer some preferred contact method. A reddit
        # username is sufficient, but nothing wrong with adding an email in here.
        UA = 'Thread Monitorer'
        r = praw.Reddit(UA)

        # return the client
        return r

    def login_to_reddit(self, user, password):
        self.client.login(user, password, disable_warning=True)

    def start(self):
        # Get multireddit object
        multireddit = self.client.get_subreddit(self.subreddits)

        while True:
            comments = multireddit.get_comments(limit=50)
            for comment in comments:
                # Check if seen comment already
                if comment.id in self.seen_comments:
                    continue
                else:
                    self.seen_comments.append(comment.id)

                return_tuple = self.check_condition(comment, self.words)
                if return_tuple[0] and not self.seen_thread(comment):
                    found_word = return_tuple[1]

                    print 'is it our first time??? ' + str(self.first_time)
                    # If it isn't our first rodeo, alert us
                    if not self.first_time:
                        self.alert(found_word.upper(), comment.permalink)

                    # Mark this thread as seen
                    self.seen_threads.append(comment.link_url)

            # Set first time to false after iterating thru comments
            self.first_time = False
            # sleep for 90 seconds, then check for new comments
            time.sleep(90)

    def check_condition(self, comment, filter_words):
        # get the string of the comment in all lowercase
        comment_text = comment.body.lower()

        # go through each of our filter words and see if it is present in this
        # comment anywhere
        for word in filter_words:
            if word in comment_text:
                return (True, word)
        return (False, '')

    def seen_thread(self, comment):
        if comment.link_url in self.seen_threads:
            return True
        else:
            return False

    def alert(self, keyword_found, permalink):
        # init the message data
        subject = 'Hey! a new comment with the word ' + keyword_found + ' was found'
        body = 'Here is the permalink to the comment: ' + permalink

        if self.user_to_alert != '':
            self.client.send_message(self.user_to_alert, subject, body)
        else:
            print subject + '\n' + body + '\n\n'
