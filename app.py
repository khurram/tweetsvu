import os
from helpers import *
from flask import Flask, request, render_template
from datetime import datetime
from twitter_text import Autolink

app = Flask(__name__)

@app.template_filter()
def time_since(tweet_time, default="just now"):
    tweet_time = datetime.strptime(tweet_time, '%a, %d %b %Y %H:%M:%S +0000')
    now = datetime.utcnow()
    diff = now - tweet_time
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default

@app.template_filter()
def sentiment_highlight(tweet):
    if tweet['polarity'] == 4:
        return 'alert-message block-message success'
    elif tweet['polarity'] == 0:
        return 'alert-message block-message error'
    elif tweet['polarity'] == 2:
        return 'alert-message block-message info'
    else:
        return 'alert-message block-message warning'

@app.template_filter()
def autolink(tweet_text):
    return Autolink(tweet_text).auto_link()
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = get_tweets(query)
    tweets = add_sentiment(tweets)
    sentiment = get_sentiment(tweets)
    tag_count = count_tags(tweets)
    user_count = count_users(tweets)
    url_count = count_urls(tweets)
    activity_count = get_activity(tweets)
    return render_template('search.html', tweets=tweets, tag_count=tag_count, 
                            user_count=user_count, url_count=url_count, 
                            activity_count=activity_count, sentiment=sentiment)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
