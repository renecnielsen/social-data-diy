'''
Parses DataSift Twitter data and counts hashtags, topics
mentions and link domains. ~2m for 1m tweets
'''
import json,csv,re,sys,os,cPickle,datetime,time,random
import glob,collections,itertools,operator

nBreak=10000
nBreak=999999999

###########
class tweetStream(object):
###########
    def __iter__(self):
        for d in glob.glob('../data/stream'):
            for f in glob.glob(d+'/Data*json'):
                fileString=open(f,'r').read().decode('utf-8')
                # Read file as one long string and convert to unicode
                for tweet in fileString.split('\n'):
                    yield json.loads(tweet)

###########
def main():
###########
    taggedHashTagCounter=collections.defaultdict(int)
    hashTagCounter=collections.defaultdict(int)
    domainCounter=collections.defaultdict(int)
    rawDomainCounter=collections.defaultdict(int)
    mentionCounter=collections.defaultdict(int)
    topicCounter=collections.defaultdict(int)
    timeCounter=collections.defaultdict(int)

    nMissingHashTags=0
    nMissingDomains=0
    nMissingRawDomains=0
    nMissingMentions=0
    nMissingTopics=0
    nMissingTaggedHashTags=0
    nMissingTimes=0
    nMultipleTaggedHashTags=0
    nMultipleTopics=0

    tweets=tweetStream()

    timeFile=open('times.txt','w')

    v=False
#    v=True

    nTweet=0

    for tweet in tweets:

        if nTweet%200000==0:print 'NTWEET',nTweet,nMultipleTopics

        if v: print tweet['interaction']['content']
        try:
            if v:print tweet['interaction']['created_at']
            parsedTime=tweet['interaction']['created_at']
            timeFile.write(parsedTime+'\t'+str(random.random())+'\n')
            # TODO figure out how to do this better
#            parsedTime=tweet['interaction']['created_at'][0:16]
#            parsedTime=parseTime.partition(' 2014')[0]
            parsedTime=' '.join(parsedTime.split(' ')[1:4])
#            print '====',parsedTime
            # Tue, 01 Jul 2014 01:36:52 +0000
            timeCounter[parsedTime]+=1
        except:
            nMissingTimes+=1

        ############
        try:
            taggedHashTags=tweet['interaction']['tag_tree']['hashtag']
            if v:print taggedHashTags
            for hashTag in taggedHashTags:
                taggedHashTagCounter[hashTag]+=1
            if len(taggedHashTags)>1:nMutlipleTaggedHashTags+=1
        except:
            nMissingTaggedHashTags+=1

        ############
        try:
            tweetTopics=tweet['interaction']['tag_tree']['topic']
            if v:print tweetTopics
            for topic in tweetTopics:
                topicCounter[topic]+=1
            if len(tweetTopics)>1:
                nMultipleTopics+=1
        except:
            nMissingTopics+=1
        ############
        try:
            tweetDomains=tweet['links']['normalized_url']
            if v:print tweetDomains
            for domain in tweetDomains:
                rawDomainCounter[domain]+=1
        except:
            nMissingRawDomains+=1
        ############
        try:
            tweetDomains=tweet['links']['domain']
            if v:print tweetDomains
            for domain in tweetDomains:
                domainCounter[domain]+=1
        except:
            nMissingDomains+=1
        #############
        try:
            tweetHashTags=tweet['interaction']['hashtags']
            if v:print tweetHashTags
            for hashTag in tweetHashTags:
                hashTagCounter[hashTag.lower()]+=1
        except:
            nMissingHashTags+=1
        ############
        try:
            tweetMentions=tweet['twitter']['mentions']
            if v:print tweetMentions
            for mention in tweetMentions:
                mentionCounter[mention.lower()]+=1
        except:
            nMissingMentions+=1


        if nTweet==nBreak:break
        nTweet+=1

    mentionCounter=sorted(mentionCounter.iteritems(),key=operator.itemgetter(1))
    hashTagCounter=sorted(hashTagCounter.iteritems(),key=operator.itemgetter(1))
    taggedHashTagCounter=sorted(taggedHashTagCounter.iteritems(),key=operator.itemgetter(1))
    domainCounter=sorted(domainCounter.iteritems(),key=operator.itemgetter(1))
    rawDomainCounter=sorted(rawDomainCounter.iteritems(),key=operator.itemgetter(1))
    topicCounter=sorted(topicCounter.iteritems(),key=operator.itemgetter(1))
    timeCounter=sorted(timeCounter.iteritems(),key=operator.itemgetter(1))

    mentionCounter.reverse()
    hashTagCounter.reverse()
    domainCounter.reverse()
    rawDomainCounter.reverse()
    topicCounter.reverse()
    timeCounter.reverse()

    print 'MENTIONS',nMissingMentions
    for m in mentionCounter[0:10]:
        print '\t',m
    print 'HASHTAGS',nMissingHashTags
    for h in hashTagCounter[0:10]:
        print '\t',h
    print 'TAGGED HASHTAGS',nMissingTaggedHashTags
    for h in taggedHashTagCounter[0:10]:
        print '\t',h

    print 'DOMAINS',nMissingDomains
    for d in domainCounter[0:10]:
        print '\t',d
    print 'TOPICS',nMissingTopics
    for t in topicCounter[0:10]:
        print '\t',t
   
    print 'TIMES',nMissingTimes
    for t in timeCounter[0:12]: # None and "" to be discarded
        print '\t',t
    print 'RAW DOMAINS',nMissingRawDomains
    for t in rawDomainCounter[0:10]:
        print '\t',t

    print 'MULTIPLE HASHTAGS',nMultipleTaggedHashTags
    print 'MULTIPLE TOPICS',nMultipleTopics
    outFile=open('DUMP_stuff.dat','w')

    cPickle.dump(mentionCounter,outFile)
    cPickle.dump(hashTagCounter,outFile)
    cPickle.dump(taggedHashTagCounter,outFile)
    cPickle.dump(domainCounter,outFile)
    cPickle.dump(topicCounter,outFile)
    cPickle.dump(timeCounter,outFile)
    cPickle.dump(rawDomainCounter,outFile)

    outFile.close()
    timeFile.close()
if __name__=='__main__':
    main()
