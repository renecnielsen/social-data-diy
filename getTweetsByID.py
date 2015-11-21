import twitter
import csv
import json

"""
NOTE: You must have python-twitter installed on the machine running this script;
	  You can install it by running this on the command line:
	  		
	  			sudo pip install python-twitter

"""

# Twitter OAuth Credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

# Establish Twitter OAuth connection
api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)

# Paths on your machine to the CSV file, and the file you'd like to output into.
csvpath = ''
tweetspath = ''

# Open the read and write files, get Status objects from read id's, write JSON objects
# to output file. Each object is separated by a newline character for easier reading.
with open(csvpath, 'rb') as csvfile:
	with open(tweetspath, 'wb') as tweetsfile:
		tweetreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
		next(tweetreader)
		for row in tweetreader:

				try:
					data = api.GetStatus(int(row[0]))
					tweetsfile.write(data.AsJsonString() + '\n')

				except: #For tweets that have been deleted since you collected their IDs
					pass
