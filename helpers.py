import requests
from twitter_text import Extractor
from operator import itemgetter

def count_tags(tweets):
    tagcount = {}
    for tweet in tweets:
        hashtags = Extractor(tweet).extract_hashtags()
        for hashtag in hashtags:
            try:
                tagcount[hashtag] += 1
            except KeyError:
                tagcount[hashtag] = 1
    tagcount = sorted(tagcount.items(), key=itemgetter(1), reverse=True)
    return tagcount

def aggregate_sentiment(tweets):
    number_of_tweets = len(tweets)
    payload = ''
    
    for tweet in tweets:
        payload += tweet['text'] + '\n'

    url = 'http://twittersentiment.appspot.com/api/bulkClassify'
    payload = payload.encode('utf8', 'xmlcharrefreplace')
    headers = {'content-type': 'text/plain; charset=utf-8'}
    r = requests.post(url, data=payload, headers=headers)

    if r.status_code == requests.codes.ok:
        posts = r.content.split('\n')
        sentiment_total = 0
        for post in posts:
            if not post == '':
                sentiment = int(post.split(',')[0].strip('"'))
                sentiment_total += sentiment
    else:
        print "Couldn't successfully access the sentiment API"
        
    avg_sentiment = (float(sentiment_total) / number_of_tweets) * 25
    return int(avg_sentiment)

def get_sentiment(tweet):
    url = 'http://twittersentiment.appspot.com/api/bulkClassify'
    payload = tweet.encode('utf8', 'xmlcharrefreplace')
    headers = {'content-type': 'text/plain; charset=utf-8'}
    r = requests.post(url, data=payload, headers=headers)
    
    if r.status_code == requests.codes.ok:
        posts = r.content.split('\n')
        for post in posts:
            if not post == '':
                sentiment = int(post.split(',')[0].strip('"'))
    return sentiment * 25.0
