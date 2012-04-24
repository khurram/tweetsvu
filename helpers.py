import json
import requests
import Queue
#from classification import classify_tweet
from datetime import datetime
from threading import Thread
from twitter import Twitter
from twitter_text import Extractor
from operator import itemgetter

def get_page_of_tweets(twitter, query, page, queue):
    queue.put(twitter.search(q=query, rpp=100, page=page)['results'])

def get_tweets(query):
    pages = 2
    threads = []
    tweets = []
    queue = Queue.Queue()
    twitter = Twitter()

    for page in range(1, pages):
        t = Thread(target=get_page_of_tweets, args=(twitter, query, page, queue))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    for thread in threads:
        tweets += queue.get()
    return tweets

def add_sentiment(tweets):
    print datetime.now(), "start add_sentiment"
    url = 'http://twittersentiment.appspot.com/api/bulkClassifyJson'
    payload = {'data': tweets}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code == requests.codes.ok:
        sentiment_tweets = json.loads(r.content)['data']
    print datetime.now(), "end add_sentiment"
    return sentiment_tweets

def get_sentiment(tweets):
    print datetime.now(), "start get_sentiment"
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
    print datetime.now(), "end get_sentiment"
    return sentiment

def get_activity(tweets):
    active_count = {}
    for tweet in tweets:
        tweet['created_at'] = tweet['created_at'][:-4] + "0100"
        print tweet['created_at'];
        t = datetime.strptime(tweet['created_at'], "%a, %d %b %Y %H:%M:%S +0100").strftime("%B %d, %Y %H:%M")
        if not t in active_count:
            active_count[t] = 0
        active_count[t] += 1
    return active_count

def count_tags(tweets):
    print datetime.now(), "start count_tags"
    tag_count = {}
    for tweet in tweets:
        tags = Extractor(tweet).extract_hashtags()
        for tag in tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
    tag_count = sorted(tag_count.items(), key=itemgetter(1), reverse=True)
    print datetime.now(), "end count_tags"
    return tag_count

def count_users(tweets):
    print datetime.now(), "start count_users"
    user_count = {}
    for tweet in tweets:
        user = tweet['from_user']
        user_count[user] = user_count.get(user, 0) + 1
    user_count = sorted(user_count.items(), key=itemgetter(1), reverse=True)
    print datetime.now(), "end count_users"
    return user_count

def count_urls(tweets):
    print datetime.now(), "start count_urls"
    url_count = {}
    for tweet in tweets:
        urls = Extractor(tweet).extract_urls()
        for url in urls:
            url_count[url] = url_count.get(url, 0) + 1
    url_count = sorted(url_count.items(), key=itemgetter(1), reverse=True)
    print datetime.now(), "end count_urls"
    return url_count

def do_sentiment(tweets):
    print datetime.now(), "start do_sentiment"
    for tweet in tweets:
        tweet['polarity'] = classify_tweet(tweet['text'])
    print datetime.now(), "end do_sentiment"

def sort_tweets(tweets):
    new_tweets = {}
    for tweet in tweets:
        time = tweet['created_at']
        new_tweets[time] = tweet
    new_tweets = sorted(new_tweets.items(), key=itemgetter(1), reverse=True)
    tweets = []
    for tweet in new_tweets:
        tweets.append(tweet)
    return new_tweets
    

def get_results(query):
    params = {}
    tweets = get_tweets(query)
    params['tweets'] = add_sentiment(tweets)
    params['sentiment'] = get_sentiment(params['tweets'])
    params['tag_count'] = count_tags(params['tweets'])
    params['user_count'] = count_users(params['tweets'])
    params['url_count'] = count_urls(params['tweets'])
    params['active_count'] = get_activity(params['tweets'])
    tweets = sort_tweets(tweets)
    return params

