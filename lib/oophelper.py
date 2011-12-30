import json
import requests
from twitter import Twitter
from twitter_text import Extractor
from operator import itemgetter

class Tweets():
    def __init__(self):
        self.tweets = []
        self.tag_count = {}
        self.user_count = {}
        self.url_count = {}
        self.sentiment = {'positive': 0, 'neutral': 0, 'negative': 0}

    def get_tweets(self, query):
        twitter = Twitter()
        for page in range(1, 6):
            self.tweets += twitter.search(q=query, rpp=100, page=page)['results']

    def add_sentiment(self):
        url = 'http://twittersentiment.appspot.com/api/bulkClassifyJson'
        payload = {'data': self.tweets}
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        if r.status_code == requests.codes.ok:
            self.tweets = json.loads(r.content)['data']

    def count_tags(self):
        for tweet in self.tweets:
            tags = Extractor(tweet).extract_hashtags()
            for tag in tags:
                self.tag_count[tag] = self.tag_count.get(tag, 0) + 1
        self.tag_count = sorted(self.tag_count.items(), key=itemgetter(1), reverse=True)

    def count_users(self):
        for tweet in self.tweets:
            user = tweet['from_user']
            self.user_count[user] = self.user_count.get(user, 0) + 1
        self.user_count = sorted(self.user_count.items(), key=itemgetter(1), reverse=True)

    def count_urls(self):
        for tweet in self.tweets:
            urls = Extractor(tweet).extract_urls()
            for url in urls:
                self.url_count[url] = self.url_count.get(url, 0) + 1
        self.url_count = sorted(self.url_count.items(), key=itemgetter(1), reverse=True)

    def get_sentiment(self):
        for tweet in self.tweets:
            if tweet['polarity'] == 4:
                self.sentiment['positive'] += 1
            elif tweet['polarity'] == 2:
                self.sentiment['neutral'] += 1
            elif tweet['polarity'] == 0:
                self.sentiment['negative'] += 1
            else:
                raise Exception('Not a valid sentiment value')
