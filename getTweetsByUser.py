"""
NOTE: You must have python-twitter installed on the machine running this script;
	  You can install it by running this on the command line:

	  			sudo pip install python-twitter
"""

import twitter, csv, json

# Twitter OAuth Credentials
# Get these be creating a new Twitter app on https://apps.twitter.com/app/new, and look
# under "Keys and Access Tokens" (https://apps.twitter.com/app/[you-twitter-app-id]/keys)
consumer_key = "" #Consumer Key (API Key)
consumer_secret = "" #Consumer Secret (API Secret)
access_token = "" #Access Token
access_secret = "" #Access Token Secret

# Establish Twitter OAuth connection
api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)

# Twitter user you want to retrieve tweets from
user = "un"

# Get tweets from Twitter API
statuses = api.GetUserTimeline(screen_name=user)

# Path on your machine to where the output JSON file should be.
# Example, Mac: /Users/[username]/Documents/twitter-analysis/data/' + user + '_tweets.json
tweetspath = ""

# Write tweets to JSON file.
# Each object is separated by a newline character for easier reading.
with open(tweetspath, "wb") as tweetsfile: #Get ready to write to output file
    json.dump([s.id for s in statuses], tweetsfile)
