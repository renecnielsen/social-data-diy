"""
NOTE: You must have Python Twitter Toolbox (https://github.com/sixohsix/twitter)
installed on the machine running this script. You can install it using
setuptools/easy_install (https://pypi.python.org/pypi/setuptools)

Run this on the command line:

	  			easy_install twitter
"""

from twitter import *
import csv, json

# Twitter OAuth Credentials
# Get these be creating a new Twitter app on https://apps.twitter.com/app/new, and look
# under "Keys and Access Tokens" (https://apps.twitter.com/app/[you-twitter-app-id]/keys)
consumer_key = "" #Consumer Key (API Key)
consumer_secret = "" #Consumer Secret (API Secret)
access_token = "" #Access Token
access_secret = "" #Access Token Secret

# Establish Twitter OAuth connection
t = Twitter(auth=OAuth(access_token, access_secret, consumer_key, consumer_secret))

# Path on your machine to the CSV file holding Tweet IDs.
# Example, Mac: /Users/[username]/Documents/twitter-analysis/src/TweetIDs.csv
csvpath = ""

# Path on your machine to where the output JSON file should be.
# Example, Mac: /Users/[username]/Documents/twitter-analysis/data/tweets.json
tweetspath = ""

# Get tweets from Twitter API by sending list of Twitter IDs, then write to JSON file.
# Each object is separated by a newline character for easier reading.
with open(csvpath, 'rb') as csvfile: #Get ready to read Tweet ID file
	with open(tweetspath, 'wb') as tweetsfile: #Get ready to write to output file
		tweetreader = csvfile.readlines()
		for row in tweetreader:
			try:
				data = t.statuses.lookup(_id=row) #Get each tweet
				json.dump(data, tweetsfile) #Write each tweet
			except: #Should something not work (blank line, only deleted tweets in line)
				pass
