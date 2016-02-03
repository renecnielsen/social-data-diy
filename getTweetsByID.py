"""
NOTE: You must have Python Twitter Toolbox (https://github.com/sixohsix/twitter)
installed on the machine running this script. You can install it using
setuptools/easy_install (https://pypi.python.org/pypi/setuptools)

Run this on the command line:

	  			easy_install twitter
"""

from twitter import *
import csv, json, sys, time
from urllib2 import URLError
from httplib import BadStatusLine
import cPickle as pickle

## Twitter OAuth Credentials
# Get these be creating a new Twitter app on https://apps.twitter.com/app/new, and look
# under "Keys and Access Tokens" (https://apps.twitter.com/app/[you-twitter-app-id]/keys)
consumer_key = "" #Consumer Key (API Key)
consumer_secret = "" #Consumer Secret (API Secret)
access_token = "" #Access Token
access_secret = "" #Access Token Secret

## Establish Twitter OAuth connection
t = Twitter(auth=OAuth(access_token, access_secret, consumer_key, consumer_secret))

## Setup Local Paths
# Paths on your machine to the CSV file, and the file you'd like to output into.
# Example csv, Mac: /Users/[username]/Documents/twitter-analysis/data/src/TweetIDs.csv
# Example pickle, Mac: /Users/[username]/Documents/twitter-analysis/data/raw/tweets.p
csvpath = '' # Path to the csv file with Tweet IDs (up to 100 IDs per line)
jsonpath = '' # Path to the JSON file where retrieved tweets go
picklepath = '' # Path to the pickle file where retrieved tweets go

## Handle HTTP Errors
# This is from Mining the Social Web, 2nd Edition (O'Reilly, 2013)

def make_twitter_request(t_func, max_errors=10, *args, **kw):

    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e

        # See https://dev.twitter.com/docs/error-codes-responses for common codes

        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429:
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return t_func(*args, **kw)
        except api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, 'URLError encountered. Continuing.'
            if error_count > max_errors:
                print >> sys.stderr, 'Too many consecutive errors...bailing out.'
                raise
        except BadStatusLine, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, 'BadStatusLine encountered. Continuing.'
            if error_count > max_errors:
                print >> sys.stderr, 'Too many consecutive errors...bailing out.'
                raise

## Get tweets
# Open the read and write files, get Status objects from read id's, write JSON
# objects to output file. Each object is separated by a newline character for 
# easier reading.
with open(csvpath, 'rb') as csvfile: #Get ready to read Tweet ID file
	with open(tweetspath, 'wb') as tweetsfile: #Get ready to write to output file
		tweetreader = csvfile.readlines()
		for row in tweetreader:
			try:
				data = t.statuses.lookup(_id=row) #Get each tweet
				json.dump(data, tweetsfile) #Write each tweet
			except: #Should something not work (blank line, only deleted tweets in line)
				pass
