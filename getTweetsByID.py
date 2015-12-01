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

# Path on your machine to the CSV file holding Tweet IDs.
csvpath = ''

# Path on your machine to where the output file should be.
tweetspath = ''

# Get tweets from Twitter API by sending list of Twitter IDs, then write to JSON file.
# Each object is separated by a newline character for easier reading.
with open(csvpath, 'rb') as csvfile: #Get ready to read Tweet ID file
	with open(tweetspath, 'wb') as tweetsfile: #Get ready to write to output file
		tweetreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
		next(tweetreader)
		for row in tweetreader:
				try:
					data = api.GetStatus(int(row[0])) #Get each tweet
					tweetsfile.write(data.AsJsonString() + '\n') #Write each tweet
				except: #For tweets that have been deleted since you collected the IDs
					pass
