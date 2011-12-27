import json
import requests
from twitter import *
from twitter_text import Extractor
from operator import itemgetter

twitter = Twitter()

def get_tweets(query):
    tweets = []
    for page in range(1, 2):
        tweets += twitter.search(q=query, rpp=100, page=page)['results']
    return tweets

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

def get_sentiment(tweets):
    url = 'http://twittersentiment.appspot.com/api/bulkClassifyJson'
    payload = {'data': tweets}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code == requests.codes.ok:
        sent_tweets = json.loads(r.content)['data']
        sentiment_total = 0
        for sent_tweet in sent_tweets:
            sentiment_total += sent_tweet['polarity']
        
    sentiment = int((float(sentiment_total) / len(tweets)) * 25)
    return sentiment, sent_tweets
