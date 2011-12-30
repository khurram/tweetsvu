import json
import requests
from twitter import Twitter
from twitter_text import Extractor
from operator import itemgetter

def get_tweets(query):
    tweets = []
    twitter = Twitter()
    for page in range(1, 6):
        tweets += twitter.search(q=query, rpp=100, page=page)['results']
    return tweets

def add_sentiment(tweets):
    url = 'http://twittersentiment.appspot.com/api/bulkClassifyJson'
    payload = {'data': tweets}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code == requests.codes.ok:
        sentiment_tweets = json.loads(r.content)['data']
    return sentiment_tweets

def count_tags(tweets):
    tag_count = {}
    for tweet in tweets:
        tags = Extractor(tweet).extract_hashtags()
        for tag in tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
    tag_count = sorted(tag_count.items(), key=itemgetter(1), reverse=True)
    return tag_count

def count_users(tweets):
    user_count = {}
    for tweet in tweets:
        user = tweet['from_user']
        user_count[user] = user_count.get(user, 0) + 1
    user_count = sorted(user_count.items(), key=itemgetter(1), reverse=True)
    return user_count

def count_urls(tweets):
    url_count = {}
    for tweet in tweets:
        urls = Extractor(tweet).extract_urls()
        for url in urls:
            url_count[url] = url_count.get(url, 0) + 1
    url_count = sorted(url_count.items(), key=itemgetter(1), reverse=True)
    return url_count

def get_sentiment(tweets):
    sentiment = {'positive': 0, 'neutral': 0, 'negative': 0}
    for tweet in tweets:
        if tweet['polarity'] == 4:
            sentiment['positive'] += 1
        elif tweet['polarity'] == 2:
            sentiment['neutral'] += 1
        elif tweet['polarity'] == 0:
            sentiment['negative'] += 1
        else:
            raise Exception('Not a valid sentiment value')
    return sentiment
